#!/usr/bin/env python
import pika, sys, os
import json
from test_acceptance.utils.datautils import DataUtils

class RabbitMqConsumer():

    def __init__(self, host, queue, exchange="pubsub"):
        self.host = host
        self.queue = queue
        self.exchange = exchange

    def main(self):
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host))
        channel = connection.channel()

        channel.exchange_declare(exchange=self.exchange, exchange_type='direct')

        result = channel.queue_declare(queue=self.queue, exclusive=True)
        queue_name = result.method.queue

        channel.queue_bind(exchange=self.exchange, queue=queue_name)

        # def on_message(rabbit_data, queue, message):
        #     rabbit_data.append(json.loads('{"queue":"%s" ,"body":%s}' % (queue, message)))

        def callback(ch, method, properties, body):
            DataUtils.rabbit_messages.append(json.loads('{"queue":"%s" ,"message":%s}'
                                                        % (json.loads(str(body, 'UTF8'))['attributes']['routingKey'], str(body, 'UTF8'))))

        channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True)
        channel.start_consuming()



