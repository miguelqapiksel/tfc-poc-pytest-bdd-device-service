#!/usr/bin/env python
import pika, sys, os
import json

class RabbitMqConsumer():

    def __init__(self, host, queue, rabbit_data=[]):
        self.host = host
        self.queue = queue
        self.rabbit_data = rabbit_data

    def main(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue)

        def on_message(rabbit_data, queue, message):
            rabbit_data.append(json.loads('{"queue":"%s" ,"body":%s}' % (queue, message)))

        def callback(ch, method, properties, body):
            print("message is----> %s" % body)

        channel.basic_consume(queue=self.queue, on_message_callback=lambda ch, method, properties,

                                                                           body: on_message(self.rabbit_data,self.queue, str(body, 'UTF8')), auto_ack=True)
        channel.start_consuming()



