import requests
from step_defs.env import Inizialization


class getMethods(object):
    def get_device_by_id(service, basicurl, headers, id):
        url = basicurl + service + "/" + id
        response = requests.get(url=url, headers=headers, verify=False)
        return response
    def get_all_devices(service, basicurl, headers):
        url = basicurl + service
        response = requests.get(url=url, headers=headers, verify=False)
        return response
    def get_conf_value(conf_value_to_be_searched):
        return Inizialization.data[':%s'% conf_value_to_be_searched]

getMethodsDevice = getMethods()