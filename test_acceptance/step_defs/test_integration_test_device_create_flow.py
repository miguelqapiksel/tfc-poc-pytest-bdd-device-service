import pytest
from pytest_bdd import scenario, given, then, when, parsers
from sttable import parse_str_table

@scenario('../features/integration_test_device_create_flow.feature', 'Integration E2E test for devices that create a flow')
def test_e2e_creates_a_flow():
     pass
@scenario('../features/integration_test_device_create_flow.feature', 'Integration E2E test for device LAWO a__madi4 does not create a flow')
def test_lawo_e2e_not_creates_a_flow():
    pass