import uuid
import random
import socket
import struct

class getDataDeviceToPost(object):
    def create_random_name(self):
        final_name = "test_device_" + str(uuid.uuid1())
        return final_name
    def create_random_ipv4(self):
        final_ipv4 = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        return final_ipv4

getDataDevice = getDataDeviceToPost()