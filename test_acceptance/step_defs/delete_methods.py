import requests
from step_defs.get_methods import getMethods

class deleteMethods(object):
    def delete_device_by_id(service, basicurl, headers, id):
        url = basicurl + service + "/" + id
        response = requests.delete(url=url, headers=headers, verify=False)
        return response
    def delete_device_by_pattern(service,basicurl,headers,pattern):
        url = basicurl + service
        all_devices=getMethods.get_all_devices(service,basicurl,headers).text
        


deleteMethodsDevice = deleteMethods()
