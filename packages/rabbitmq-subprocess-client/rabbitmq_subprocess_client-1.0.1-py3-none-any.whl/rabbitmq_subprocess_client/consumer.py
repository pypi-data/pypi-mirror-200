import _thread
import functools
import logging
from concurrent.futures import as_completed
from concurrent.futures import ProcessPoolExecutor
from urllib.parse import urlparse

import pika

from .utils import timeout


LOGGER = logging.getLogger(__name__)


class Consumer:
    """
    This is the class managing the RabbitMQ
    """

    def __init__(self, queue_name, host, port, user, password, timeout=None, queue_type=None):
        """Create a new instance of the consumer class, passing in the AMQP
        URL used to connect to RabbitMQ.

        :param str amqp_url: The AMQP url to connect with

        """
        self.should_reconnect = False
        self.was_consuming = False
        self.QUEUE = queue_name
        self.queue_args = {}
        if queue_type is not None:
            self.queue_args["x-queue-type"] = queue_type
        self._connection = None
        self._channel = None
        self._closing = False
        self._consumer_tag = None
        self._url = "amqp://%s:%s@%s:%s/%s" % (
            user,
            password,
            host,
            port,
            "%2f",
        )
        self._consuming = False
        # In production, experiment with higher prefetch values
        # for higher consumer throughput
        self._prefetch_count = 1

        self.timeout = timeout

    def connect(self):
        """This method connects to RabbitMQ, returning the connection handle.
        When the connection is established, the on_connection_open method
        will be invoked by pika.

        :rtype: pika.SelectConnection

        """
        parsed_url = urlparse(self._url)
        LOGGER.info("Connecting to %s:%s", parsed_url.hostname, parsed_url.port)
        return pika.SelectConnection(
            parameters=pika.URLParameters(self._url),
            on_open_callback=self.on_connection_open,
            on_open_error_callback=self.on_connection_open_error,
            on_close_callback=self.on_connection_closed,
        )

    def close_connection(self):
        LOGGER.info("Close connection")
        self._consuming = False
        if self._connection.is_closing or self._connection.is_closed:
            LOGGER.info("Connection is closing or already closed")
        else:
            LOGGER.info("Closing connection")
            self._connection.close()

    def on_connection_open(self, _unused_connection):
        """This method is called by pika once the connection to RabbitMQ has
        been established. It passes the handle to the connection object in
        case we need it, but in this case, we'll just mark it unused.

        :param pika.SelectConnection _unused_connection: The connection

        """
        LOGGER.info("Connection opened")
        self.open_channel()

    def on_connection_open_error(self, _unused_connection, err):
        """This method is called by pika if the connection to RabbitMQ
        can't be established.

        :param pika.SelectConnection _unused_connection: The connection
        :param Exception err: The error

        """
        LOGGER.error("Connection open failed: %s", err)
        self.should_reconnect = True
        self.reconnect()
        raise ConnectionError(err)

    def on_connection_closed(self, _unused_connection, reason):
        """This method is invoked by pika when the connection to RabbitMQ is
        closed unexpectedly. Since it is unexpected, we will reconnect to
        RabbitMQ if it disconnects.

        :param pika.connection.Connection connection: The closed connection obj
        :param Exception reason: exception representing reason for loss of
            connection.

        """
        LOGGER.info("Stopping ioloop and reconnecting")
        self._channel = None
        if self._closing:
            self._connection.ioloop.stop()
        else:
            LOGGER.warning("Connection closed, reconnect necessary: %s", reason)
            self.reconnect()

    def reconnect(self):
        """Will be invoked if the connection can't be opened or is
        closed. Indicates that a reconnect is necessary then stops the
        ioloop.

        """
        self.should_reconnect = True
        self.stop()

    def open_channel(self):
        """Open a new channel with RabbitMQ by issuing the Channel.Open RPC
        command. When RabbitMQ responds that the channel is open, the
        on_channel_open callback will be invoked by pika.

        """
        LOGGER.info("Creating a new channel")
        self._connection.channel(on_open_callback=self.on_channel_open)

    def on_channel_open(self, channel):
        """This method is invoked by pika when the channel has been opened.
        The channel object is passed in so we can make use of it.

        Since the channel is now open, we'll declare the queue to use.

        :param pika.channel.Channel channel: The channel object

        """
        LOGGER.info("Channel opened")
        self._channel = channel
        self.add_on_channel_close_callback()

        LOGGER.info("Declaring queue %s", self.QUEUE)
        cb = functools.partial(self.on_queue_declareok, userdata=self.QUEUE)
        self._channel.queue_declare(
            queue=self.QUEUE,
            callback=cb,
            durable=True,
            arguments=self.queue_args,
        )

    def add_on_channel_close_callback(self):
        """This method tells pika to call the on_channel_closed method if
        RabbitMQ unexpectedly closes the channel.

        """
        LOGGER.info("Adding channel close callback")
        self._channel.add_on_close_callback(self.on_channel_closed)

    def on_channel_closed(self, channel, reason):
        """Invoked by pika when RabbitMQ unexpectedly closes the channel.
        Channels are usually closed if you attempt to do something that
        violates the protocol, such as re-declare an exchange or queue with
        different parameters. In this case, we'll close the connection
        to shutdown the object.

        :param pika.channel.Channel: The closed channel
        :param Exception reason: why the channel was closed

        """
        LOGGER.warning("Channel %i was closed: %s", channel, reason)
        self.close_connection()

    def on_queue_declareok(self, _unused_frame, userdata):
        """Method invoked by pika when the Queue.Declare RPC call made in
        setup_queue has completed. In this method we will bind the queue
        and exchange together with the routing key by issuing the Queue.Bind
        RPC command. When this command is complete, the on_bindok method will
        be invoked by pika.

        :param pika.frame.Method _unused_frame: The Queue.DeclareOk frame
        :param str|unicode userdata: Extra user data (queue name)

        """
        self.set_qos()

    def set_qos(self):
        """This method sets up the consumer prefetch to only be delivered
        one message at a time. The consumer must acknowledge this message
        before RabbitMQ will deliver another one. You should experiment
        with different prefetch values to achieve desired performance.

        """
        self._channel.basic_qos(
            prefetch_count=self._prefetch_count, callback=self.on_basic_qos_ok
        )

    def on_basic_qos_ok(self, _unused_frame):
        """Invoked by pika when the Basic.QoS method has completed. At this
        point we will start consuming messages by calling start_consuming
        which will invoke the needed RPC commands to start the process.

        :param pika.frame.Method _unused_frame: The Basic.QosOk response frame

        """
        LOGGER.info("QOS set to: %d", self._prefetch_count)
        self.start_consuming()

    def start_consuming(self):
        """This method sets up the consumer by first calling
        add_on_cancel_callback so that the object is notified if RabbitMQ
        cancels the consumer. It then issues the Basic.Consume RPC command
        which returns the consumer tag that is used to uniquely identify the
        consumer with RabbitMQ. We keep the value to use it when we want to
        cancel consuming. The on_message method is passed in as a callback pika
        will invoke when a message is fully received.

        """
        LOGGER.info("Issuing consumer related RPC commands")
        self.add_on_cancel_callback()
        self._consumer_tag = self._channel.basic_consume(self.QUEUE, self.on_message)
        self.was_consuming = True
        self._consuming = True

    def add_on_cancel_callback(self):
        """Add a callback that will be invoked if RabbitMQ cancels the consumer
        for some reason. If RabbitMQ does cancel the consumer,
        on_consumer_cancelled will be invoked by pika.

        """
        LOGGER.info("Adding consumer cancellation callback")
        self._channel.add_on_cancel_callback(self.on_consumer_cancelled)

    def on_consumer_cancelled(self, method_frame):
        """Invoked by pika when RabbitMQ sends a Basic.Cancel for a consumer
        receiving messages.

        :param pika.frame.Method method_frame: The Basic.Cancel frame

        """
        LOGGER.info("Consumer was cancelled remotely, shutting down: %r", method_frame)
        if self._channel:
            self._channel.close()

    def acknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        LOGGER.info("Acknowledging message %s", delivery_tag)
        self._channel.basic_ack(delivery_tag)

    def nacknowledge_message(self, delivery_tag):
        """Acknowledge the message delivery from RabbitMQ by sending a
        Basic.Ack RPC method for the delivery tag.

        :param int delivery_tag: The delivery tag from the Basic.Deliver frame

        """
        LOGGER.info("Nacknowledging message %s", delivery_tag)
        self._channel.basic_nack(delivery_tag, requeue=False)

    def stop_consuming(self):
        """Tell RabbitMQ that you would like to stop consuming by sending the
        Basic.Cancel RPC command.

        """
        if self._channel:
            LOGGER.info("Sending a Basic.Cancel RPC command to RabbitMQ")
            cb = functools.partial(self.on_cancelok, userdata=self._consumer_tag)
            self._channel.basic_cancel(self._consumer_tag, cb)

    def on_cancelok(self, _unused_frame, userdata):
        """This method is invoked by pika when RabbitMQ acknowledges the
        cancellation of a consumer. At this point we will close the channel.
        This will invoke the on_channel_closed method once the channel has been
        closed, which will in-turn close the connection.

        :param pika.frame.Method _unused_frame: The Basic.CancelOk frame
        :param str|unicode userdata: Extra user data (consumer tag)

        """
        self._consuming = False
        LOGGER.info("RabbitMQ acknowledged the cancellation of the consumer: %s", userdata)
        self.close_channel()

    def close_channel(self):
        """Call to close the channel with RabbitMQ cleanly by issuing the
        Channel.Close RPC command.

        """
        LOGGER.info("Closing the channel")
        self._channel.close()

    def run(self):
        """Run the example consumer by connecting to RabbitMQ and then
        starting the IOLoop to block and allow the SelectConnection to operate.

        """
        LOGGER.info("run")
        self._connection = self.connect()
        self._connection.ioloop.start()

    def stop(self):
        """Cleanly shutdown the connection to RabbitMQ by stopping the consumer
        with RabbitMQ. When RabbitMQ confirms the cancellation, on_cancelok
        will be invoked by pika, which will then closing the channel and
        connection. The IOLoop is started again because this method is invoked
        when CTRL-C is pressed raising a KeyboardInterrupt exception. This
        exception stops the IOLoop which needs to be running for pika to
        communicate with RabbitMQ. All of the commands issued prior to starting
        the IOLoop will be buffered but not processed.

        """
        LOGGER.info("stop")
        if not self._closing:
            self._closing = True
            LOGGER.info("Stopping")
            if self._consuming:
                self.stop_consuming()
            elif self._connection:
                self._connection.ioloop.stop()
            LOGGER.info("Stopped")

    def on_message(self, _unused_channel, basic_deliver, properties, body):
        """Invoked by pika when a message is delivered from RabbitMQ. The
        channel is passed for your convenience. The basic_deliver object that
        is passed in carries the exchange, routing key, delivery tag and
        a redelivered flag for the message. The properties passed in is an
        instance of BasicProperties with the message properties and the body
        is the message that was sent.

        :param pika.channel.Channel _unused_channel: The channel object
        :param pika.Spec.Basic.Deliver: basic_deliver method
        :param pika.Spec.BasicProperties: properties
        :param bytes body: The message body

        """
        LOGGER.info(
            "Received message # %s from %s: %s",
            basic_deliver.delivery_tag,
            properties.app_id,
            body,
        )

        def run_thread():
            self.consume_main(basic_deliver, body)

        _thread.start_new_thread(run_thread, ())

    def exec(self, msg, *args, **kwargs):
        with ProcessPoolExecutor(max_workers=1) as executor:
            future = executor.submit(
                self._consume_subprocess, self.timeout, msg, *args, **kwargs
            )
            next(as_completed([future])).result()

    @classmethod
    def _consume_subprocess(cls, time, msg, *args, **kwargs):
        with timeout(time):
            cls.consume_subprocess(msg, *args, **kwargs)

    def consume_main(self, basic_deliver, msg):
        raise NotImplementedError("You must implement this method")

    @staticmethod
    def consume_subprocess(msg, *args, **kwargs):
        raise NotImplementedError("You must implement this method")
