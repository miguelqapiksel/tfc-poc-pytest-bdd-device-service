import threading

import yaml
from test_acceptance.utils.rabbitconsumer import RabbitMqConsumer


class Inizialization():
    with open('../config/env_conf.yaml') as f:
        try:
            data = yaml.load(f, Loader=yaml.FullLoader)
            rabbit_consumer = RabbitMqConsumer(data[':rabbit_mq_adress'], data[':rabbit_mq_queue'])
            tr = threading.Thread(target=rabbit_consumer.main,
                              daemon=True)
            tr.start()
        except yaml.YAMLError as exc:
            print(exc)