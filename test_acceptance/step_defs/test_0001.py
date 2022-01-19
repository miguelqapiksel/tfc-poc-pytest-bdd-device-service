import pytest

from pytest_bdd import scenario, given, when, then, parsers


@scenario('../features/WebApi.feature', 'get all devices')
def test_retrieve():
    pass



