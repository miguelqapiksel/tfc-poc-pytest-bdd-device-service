import threading

import yaml
import logging
from utils.rabbitconsumer import RabbitMqConsumer


class Inizialization():
    with open('../config/env_conf.yaml') as f:
        try:
            data = yaml.load(f, Loader=yaml.FullLoader)
            threads = list()
            for queue in data[':mq_queues'].split(","):
                rabbit_consumer = RabbitMqConsumer(data[':mq_adress'], queue)
                tr = threading.Thread(target=rabbit_consumer.main,
                                      daemon=True)
                threads.append(tr)
                tr.start()


        except yaml.YAMLError as exc:
            print(exc)