import os
import allure
import threading
from pathlib import Path
import time

import pytest
from string import Template
import json
from pytest_bdd import scenario, given, when, then, parsers
from test_acceptance.config.env import Inizialization
from test_acceptance.step_defs.datatable import datatable
from test_acceptance.step_defs.delete_methods import deleteMethods
from test_acceptance.step_defs.get_methods import getMethods
from test_acceptance.utils.rabbitmocksender import RabbitMockSender
from test_acceptance.utils.datautils import DataUtils
from test_acceptance.step_defs.data_device_post import getDataDeviceToPost
from test_acceptance.config.env import Inizialization
from test_acceptance.step_defs.datatable import datatable
from test_acceptance.step_defs.delete_methods import deleteMethods
from test_acceptance.step_defs.get_methods import getMethods
from test_acceptance.utils.rabbitmocksender import RabbitMockSender
from test_acceptance.utils.datautils import DataUtils
from test_acceptance.step_defs.data_device_post import getDataDeviceToPost
from test_acceptance.utils.mysqldatabase import mysqlDataBase
from test_acceptance.utils.rabbitconsumer import RabbitMqConsumer
import ssl
from sttable import parse_str_table
from dotmap import DotMap
import requests

from test_acceptance.utils.rabbitconsumer import RabbitMqConsumer

api_endpoints = {}
request_headers = {}
response_codes = {}
response_texts = {}
request_bodies = {}
api_url = None
threads = []

@given('I initialize REST API main params')
@allure.step
def api_initialization():
    global api_url
    global service
    global headers
    global manager
    global ipv4
    global dbmanager
    api_url = Inizialization.data[':basic_url']
    service = Inizialization.data[':service']
    request_headers['X-Context'] = Inizialization.data[':header_x_context']
    request_headers['X-Production_Id'] = Inizialization.data[':header_x_production_id_default']
    headers = request_headers
    manager = getDataDeviceToPost()
    dbmanager = mysqlDataBase(Inizialization.data[':device_data_base'][':host'],
                              Inizialization.data[':device_data_base'][':port'],
                              Inizialization.data[':device_data_base'][':user'],
                              Inizialization.data[':device_data_base'][':data_base_name'])


# START POST Scenario
@given('I Set POST api endpoint')
@allure.step
def endpoint_to_post():
    api_endpoints['POST_URL'] = api_url + service
    print('url :' + api_endpoints['POST_URL'])


#You may also include "And" or "But" as a step - these are renamed by behave to take the name of their preceding step, so:
@when(parsers.parse('Set request Body from {file} using the data:\n{table_with_header}'))
@allure.step
def set_request_body(file,datatable, table_with_header):
    expected_table = parse_str_table(table_with_header)
    keys = expected_table.get_column(0)
    values = expected_table.get_column(1)
    # print(eval(manager.create_random_name()))
    value_evaluate = []
    for data in values:
        if DataUtils.is_a_command(data):
        #   print("the data is")
        #    print(data)
            value_evaluate.append(eval(data))
        else:
            value_evaluate.append(data)
    dict_param_value = dict(zip(keys, value_evaluate))
    with open(Inizialization.data[':basic_path_template'] + file, 'r') as json_file:
        content = ''.join(json_file.readlines())
        template = Template(content)
        configuration = json.loads(template.substitute(dict_param_value))
        print(configuration)
    request_bodies['POST'] = configuration


# You may also include "And" or "But" as a step - these are renamed by behave to take the name of their preceding step, so:
@when('Send POST HTTP request')
@allure.step
def send_post():
    try:
        response = requests.post(url=api_endpoints['POST_URL'], json=request_bodies['POST'], headers=headers,
                                 verify=False)
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)

    response_texts['POST'] = response.text
    DataUtils.set_last_response(response.text)
    DataUtils.resources.append(response.text)
    print("post response :" + response.text)
    # extracting response status_code
    statuscode = response.status_code
    response_codes['POST'] = statuscode


@then('I receive valid HTTP response code 201')
@allure.step
def receive_valid_http_response():
    print('Post rep code ;' + str(response_codes['POST']))
    assert response_codes['POST'] is 201


# END POST Scenario

# START GET Scenario
@given(parsers.cfparse('I Set GET posts api endpoint {id:Char}', extra_types=dict(Char=str)))
@allure.step
def set_get_api_endpoint(id):
    api_endpoints['GET_URL'] = api_url + '/posts/' + id
    print('url :' + api_endpoints['GET_URL'])


@given('I Set GET devices api endpoint')
@allure.step
def set_get_api_endpoint():
    api_endpoints['GET_URL'] = api_url + service
    print('url :' + api_endpoints['GET_URL'])


# You may also include "And" or "But" as a step - these are renamed by behave to take the name of their preceding step, so:
@when(parsers.cfparse('Send GET HTTP request to {service_name:Char} service', extra_types=dict(Char=str)))
@allure.step
def send_get_http_request(service_name):
    # sending get request and saving response as response object
    # print("--------------------------")
    # print(api_endpoints['GET_URL'])
    # print(headers)
    # print("-------------------------------")

    response = requests.get(url=api_endpoints['GET_URL'], headers=headers,
                            verify=False)  # https://jsonplaceholder.typicode.com/posts
    DataUtils.last_response = json.loads(response.text)['results']
    # extracting response text
    # response_texts['GET'] = response.text
    # extracting response status_code
    statuscode = response.status_code
    response_codes['GET'] = statuscode
     # DataUtils.last_response['GET'] = response.text


@when('I send a GET HTTP request by id to the device service')
@allure.step
def send_get_http_request_by_id():
    json_device = json.loads(response_texts['POST'])
    response = getMethods.get_device_by_id(service, api_url, headers, json_device["id"])
    DataUtils.last_response['GET'] = response.text
    response_texts['GET'] = response.text


@then(parsers.cfparse('I receive valid HTTP response code 200 for {request_name:Char}', extra_types=dict(Char=str)))
@allure.step
def receive_valid_http_response_code_200(request_name):
    print('Get rep code for ' + request_name + ':' + str(response_codes[request_name]))
    assert response_codes[request_name] is 200


@then(parsers.parse('verify response attributes:\n{one_col_table_w_header}'))
@allure.step
def verify_response_attribute_values_one_column(datatable, one_col_table_w_header):
    expected_table = parse_str_table(one_col_table_w_header)
    jsonResponse = json.loads(response_texts['GET'])
    print(jsonResponse['results'][0])
    for x in expected_table.get_column(0):
        # for y in expected_table.get_column(1):
        print(x)
    #     if not x in jsonResponse['results'][0]: raise Exception('the field:'+ x + ' is not in the response')
    #     exec(y)


# @then(parsers.parse('last response should contain:\n{table_with_header}'))
# def verify_response_attribute_values_several_columns(datatable, table_with_header):
#     expected_table = parse_str_table(table_with_header)
#     jsonResponse = json.loads(response_texts['GET'])
#     print(jsonResponse['results'][0])
#     iterator = 0
#     while iterator < len(expected_table.rows):
#         field_expected = expected_table.get_column(0)[iterator]
#         expected_data = expected_table.get_column(1)[iterator]
#
#         if not field_expected in jsonResponse['results'][0]: raise Exception('the field:' + field_expected + ' is not in the response')
#         exec(expected_data)
#         iterator += 1


@given(parsers.cfparse('I send a mock message with {mock_message:Char} in RabbitMQ to routing key {routing_key:Char}',
                       extra_types=dict(Char=str)))
@allure.step
def send_message_to_rabbitmq(mock_message, routing_key):
    rabbit_mq_handler = RabbitMockSender(Inizialization.data[':mq_adress'], routing_key,
                                         mock_message)

    rabbit_mq_handler.send_message()
    time.sleep(10)  # This is just for mocking, since rabbitmq messages is not a thing that happens in ms


@given(parsers.cfparse(
    'I send a mock message from json file {json_file_path} in RabbitMQ to routing key {routing_key:Char}',
    extra_types=dict(Char=str)))
@allure.step
def send_message_to_rabbitmq_from_json_file(json_file_path, routing_key):
    with open(json_file_path, 'r') as j:
        json_file_content = j.read()

    rabbit_mq_handler = RabbitMockSender(Inizialization.data[':mq_adress'], routing_key,
                                         json_file_content)

    rabbit_mq_handler.send_message()
    time.sleep(10)  # This is just for mocking, since rabbitmq messages is not a thing that happens in ms


@then(parsers.cfparse('I check message {message:Char} exists in RabbitMQ for routing key {routing_key:Char}',
                      extra_types=dict(Char=str)))
@allure.step
def send_message_to_rabbitmq(message, routing_key):
    start_time = time.time()
    seconds = int(Inizialization.data[':pool_messages_minutes_timeout']) * 60
    timeout_reached = False
    message_found = False

    while not timeout_reached and not message_found:
        if len(Inizialization.rabbit_consumer.rabbit_data) > 0:
            for rabbit_message in Inizialization.rabbit_consumer.rabbit_data:
                if rabbit_message['queue'] in routing_key:
                    if rabbit_message['body'] == json.loads(message):
                        message_found = True

        # print ("keep pooling, there are no messages in the queue")
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            timeout_reached = True
            time.sleep(3)

    assert message_found == True, 'message %s was not found in %s routing key' % (message, routing_key)


@then(parsers.parse(
    'I check message sent to RabbitMQ for routing key {routing_key} should contain:\n{table_with_header}'))
@allure.step
def verify_message_rabbit_mq_values_several_columns(routing_key, datatable, table_with_header):
    expected_table = parse_str_table(table_with_header)
    start_time = time.time()
    seconds = int(Inizialization.data[':pool_messages_minutes_timeout']) * 60
    timeout_reached = False
    message_found = False
    expectations_not_match = False

    while not timeout_reached and not message_found and not expectations_not_match:
        if len(DataUtils.rabbit_messages) > 0:
            for rabbit_message in DataUtils.rabbit_messages:
                if rabbit_message['queue'] in routing_key \
                        and DataUtils.return_device_id_from_rabbit_message(rabbit_message) in \
                        json.loads(response_texts['POST'])['id']:
                    print("MQ-MESSAGE:---->%s" % DataUtils.rabbit_messages)
                    iterator = 0
                    while iterator < len(expected_table.rows):
                        field_expected = expected_table.get_column(0)[iterator]
                        expected_data = expected_table.get_column(1)[iterator]
                        if DataUtils.is_a_command(expected_data):
                            expected_data = eval(expected_data)
                        field_value = DataUtils.convert_field_expected_to_dict(
                            field_expected, rabbit_message['message'])
                        if field_value is not None:
                            if expected_data in field_value:
                                message_found = True
                            else:
                                expectations_not_match = True  # This is going to force the loop since one of the expectation was not matched
                                if expectations_not_match: raise Exception(
                                    'the value for: %s was different from the expected one --> %s != %s' % (
                                        field_expected, expected_data, field_value))
                        iterator += 1

        # print ("keep pooling, there are no messages in the queue")
        current_time = time.time()
        elapsed_time = current_time - start_time
        if elapsed_time > seconds:
            timeout_reached = True
            time.sleep(3)

    if not message_found:
        raise Exception(
            'Field/s expected was not found in %s routing key' % routing_key)


@when(parsers.cfparse('I Send a GET HTTP request to {service:Char} with {request:Char}', extra_types=dict(Char=str)))
@allure.step
def send_get_http_request(service, request):
    # sending get request and saving response as response object
    print("--------------------------")
    print(Inizialization.data[':%s_url' % service])
    print(headers)
    print('Get from --> %s' % Inizialization.data[':%s_url' % service]
          + DataUtils.convert_request(request))
    print("-------------------------------")
    retries = 0
    empty_body = True

    while retries < int(Inizialization.data[':retries_requests']) and empty_body:
        try:
            response = requests.get(url=Inizialization.data[':%s_url' % service]
                                        + DataUtils.convert_request(request), headers=headers,
                                    verify=False)  # https://jsonplaceholder.typicode.com/posts
            if json.loads(response.text)['results'] == []:
                print("Request attempt %s" % str(retries + 1))
                time.sleep(3)
            else:
                empty_body = False
            retries += 1
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

    # extracting response text
    response_texts['GET'] = response.text
    print("Response from GET ---> : %s" % response.text)
    DataUtils.set_last_response(response.text)
    # extracting response status_code
    statuscode = response.status_code
    response_codes['GET'] = statuscode


@then(parsers.parse('last response should contain:\n{table_with_header}'))
@allure.step
def last_response_check(datatable, table_with_header):
    expected_table = parse_str_table(table_with_header)

    message_found = False
    expectations_not_match = False

    while not message_found and not expectations_not_match:
        if len(DataUtils.last_response) > 0:
            iterator = 0
            while iterator < len(expected_table.rows):
                field_expected = expected_table.get_column(0)[iterator]
                expected_data = expected_table.get_column(1)[iterator]
                if DataUtils.is_a_command(expected_data):
                    expected_data = eval(expected_data)
                field_value = DataUtils.convert_field_expected_to_dict_last_response(
                    field_expected, DataUtils.last_response)
                if field_value is not None:
                    if expected_data in field_value:
                        message_found = True
                    else:
                        expectations_not_match = True  # This is going to force the loop since one of the expectation was not matched
                        if expectations_not_match: raise Exception(
                            'the value for: %s was different from the expected one --> %s != %s' % (
                                field_expected, expected_data, field_value))
                iterator += 1

    if not message_found:
        raise Exception(
            'Value/s expected was not found in %s routing key')


@then(parsers.parse('last response should be empty'))
@allure.step
def last_response_check_empty():
    if not DataUtils.last_response == []:
        raise Exception(
            'Last response has data in it %s' % DataUtils.last_response)


@then(parsers.parse('last response should not be empty'))
@allure.step
def last_response_check_no_empty():
    if DataUtils.last_response == []:
        raise Exception(
            'Last response has no data in it ')


# ---------------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------Set Up-------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#
def pytest_sessionstart():
    rabbit_consumer = RabbitMqConsumer(Inizialization.data[':mq_adress'], Inizialization.data[':mq_queues'])
    tr = threading.Thread(target=rabbit_consumer.main,
                          daemon=True)
    threads.append(tr)
    tr.start()


# ---------------------------------------------------Data Base ---------------------------------------------------------#
@when('I check that the new device created is stored in database')
@allure.step
def check_device_id_in_database():
    json_device = json.loads(response_texts['POST'])
    id = json_device['id']
    query = "SELECT * FROM device WHERE id = UNHEX(REPLACE('{id}', '-', ''));".format(id=id)
    result_query = dbmanager.execute_query(query)
    assert (json_device['name'] in result_query[0])


# ---------------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------To be deleted---------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#


@given(parsers.cfparse('I run {scr:Char} scenario', extra_types=dict(Char=str)))
def i_run_scenario(scr):
    print("\n\033[2;32;43m" + "Currently running " + scr + " scenario!" + "\033[0;0m")

# ---------------------------------------------------------------------------------------------------------------------#
# -----------------------------------------------Tear Down-------------------------------------------------------------#
# ---------------------------------------------------------------------------------------------------------------------#
def pytest_sessionfinish(session, exitstatus):
    print("\n-----------Deleting devices created-------------------")
    print(type(DataUtils.resources))
    if len(DataUtils.resources) != 0:
        for device in DataUtils.resources:
            json_device = json.loads(device)
            if getMethods.get_device_by_id(service, api_url, headers, json_device["id"]).status_code == 200:
                deleteMethods.delete_device_by_id(service, api_url, headers, json_device["id"])
                #deleteMethods.delete_device_by_pattern(service, api_url, headers, Inizialization.data[':pattern'])
                


@pytest.fixture(autouse=True, scope='session')
def delete_device_created():
    def my_fixture():
        # setup_stuff
        yield
        # teardown_stuff
