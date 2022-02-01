import uuid
import random
import socket
import struct
import rstr

class getDataDeviceToPost(object):
    def create_random_name(self):
        final_name = "test_device_" + str(uuid.uuid1())
        return final_name
    def create_random_ipv4(self):
        final_ipv4 = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        return final_ipv4
    def create_random_mc_value(self):
        mc_value = rstr.xeger(r'^2(?:2[4-9]|3\d)(?:\.(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d?|0)){3}$')
        return mc_value
    def create_random_io_value(self):
        io_value = rstr.xeger(r'^(?:1?\d|20)$')
        return io_value
    def create_random_configuration_option(self):
        conf_option = rstr.xeger(r'^(AHS_AVP_WAN|AHS_DMV_4K|AHS_DMV_HD|AOT_GFX|AOT_HOST|FWC_AVP|FWC_CENT_DMV|FWC_EMERG|FWC_HDR_SDR|FWC_LIVE_DMV|FWC_HBS_AVP|FWC_HBS_DMV|FWC_UDX|GIR_DMV|LI_DMV|LI_DMV_SINGLE|LI_Streamer|MELB_AVP_Lab|NL_CPT_AVP_Gateway_10x10|NL_CPT_AVP_Streamer|NL_CPT_AVP_ESPN_Shuffler|NL_CPT_DMV_ESPN|NL_CPT_DMV_LC|NL_CPT_DMV_PCR|NL_CPT_AVP_MIXER|OBC_UEFA_MCR_DMV|OBC_UEFA_MCR_AVP|SRT3_AVP_Gateway_2|SRT3_AVP_Gateway_8|SRT3_AVP_Gateway_8M|SRT3_AVP_Gateway_10|SRT3_AVP_Gateway_18|SRT3_AVP_Gateway_16|SRT3_DMV|SS5_AVP_Gateway_8|SS5_AVP_Gateway_12|SS5_AVP_Shuffler|SS5_DMV|SS5_DMV_Baseband|SS5_UDX|SS9_AVP|SS9_DMV|SS9_UTIL)$')
        return conf_option


getDataDevice = getDataDeviceToPost()