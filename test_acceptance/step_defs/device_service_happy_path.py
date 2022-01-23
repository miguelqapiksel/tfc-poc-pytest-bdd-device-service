import pytest
from pytest_bdd import scenario, given, then, when, parsers
from sttable import parse_str_table

# @scenario('../features/device_service.feature', 'get all devices')
# def test_get_all_devices():
#      pass
@scenario('../features/device_service.feature', 'Test rabbit MQ messages')
def test_rabbit_mq_messages():
     pass


