import threading

import yaml
import logging


class Inizialization():
    with open('../config/env_conf.yaml') as f:
        try:
            data = yaml.load(f, Loader=yaml.FullLoader)

        except yaml.YAMLError as exc:
            print(exc)

