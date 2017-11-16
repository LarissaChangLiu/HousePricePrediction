"""cloudAMQP_client"""
import json
import pika


class CloudAMQPClient(object):
    """cloudAMQP_client"""
    def __init__(self, cloud_amqp_url, queue_name):
        self.cloud_amqp_url = cloud_amqp_url
        self.queue_name = queue_name
        self.params = pika.URLParameters(cloud_amqp_url)
        self.params.socket_timeout = 1200
        self.connection = pika.BlockingConnection(
            self.params)  # Connect to CloudAMQP
        self.channel = self.connection.channel()  # start a channel
        self.channel.queue_declare(queue=queue_name)  # Declare a queue

    def send_message(self, message):
        """sent_message"""
        self.channel.basic_publish(exchange='', routing_key=self.queue_name,
                                   body=json.dumps(message))
        print ("[x] Sent message to %s: %s" % (self.queue_name, message))

    def get_message(self):
        """get_message"""
        method_frame, _, body = self.channel.basic_get(self.queue_name)

        if method_frame:
            print ("[x] Received message from %s: %s" % (self.queue_name, body))
            self.channel.basic_ack(method_frame.delivery_tag)
            return json.loads(body.decode("utf-8"))
        else:
            print ("No message returned")
            return None

    # BlockingConnection.sleep is a safer way to sleep than time.sleep(). This
    # will repond to server's heartbeat.
    def sleep(self, seconds):
        """sleep"""
        self.connection.sleep(seconds)
