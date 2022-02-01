import pytest
from pytest_bdd import scenario, given, then, when, parsers
from sttable import parse_str_table

@scenario('../features/post_device_service.feature', 'post one device in device service')
def test_e2e_post_device():
     pass