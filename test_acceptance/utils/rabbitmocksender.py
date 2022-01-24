import pika

class RabbitMockSender():

    def __init__(self, host, queue, message_to_send="", exchange=""):
        self.host = host
        self.queue = queue
        self.exchange = exchange
        self.message_to_send = message_to_send

    def send_message(self):
        connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=self.host))
        channel = connection.channel()

        channel.queue_declare(queue=self.queue)

        channel.basic_publish(exchange=self.exchange, routing_key=self.queue, body=self.message_to_send)
        connection.close()


