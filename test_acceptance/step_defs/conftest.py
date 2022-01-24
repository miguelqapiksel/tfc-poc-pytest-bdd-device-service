import pytest
from string import Template
import json
from pytest_bdd import scenario, given, when, then, parsers
from step_defs.env import Inizialization
from step_defs.datatable import datatable
from utils.datautils import DataUtils
import ssl
from sttable import parse_str_table
import requests


api_endpoints = {}
request_headers = {}
response_codes ={}
response_texts={}
request_bodies = {}
api_url=None


@given('I set sample REST API url')
def api_initialization():
    global api_url
    global service
    global headers
    api_url = Inizialization.data[':basic_url']
    service = Inizialization.data[':service']
#    request_headers['Content-Type'] = Inizialization.data[':header_content_type']
    request_headers['X-Context'] = Inizialization.data[':header_x_context']
    request_headers['X-Production_Id'] = Inizialization.data[':header_x_production_id_default']
    headers=request_headers

# START POST Scenario
@given('I Set POST api endpoint')
def endpoint_to_post():
    api_endpoints['POST_URL'] = api_url + service
    print('url :'+api_endpoints['POST_URL'])

#You may also include "And" or "But" as a step - these are renamed by behave to take the name of their preceding step, so:
@when(parsers.parse('Set request Body using the data:\n{table_with_header}'))
def set_request_body(datatable,table_with_header):
    expected_table = parse_str_table(table_with_header)
    keys=expected_table.get_column(0)
    values=expected_table.get_column(1)
    dict_param_value=dict(zip(keys,values))
    with open('../data/resources/templates/device_template.json', 'r') as json_file:
        content = ''.join(json_file.readlines())
        template = Template(content)
        configuration = json.loads(template.substitute(dict_param_value))
        print(configuration)
    request_bodies['POST']=configuration

#You may also include "And" or "But" as a step - these are renamed by behave to take the name of their preceding step, so:
@when('Send POST HTTP request')
def send_post():
    response = requests.post(url=api_endpoints['POST_URL'], json=request_bodies['POST'], headers=headers, verify=False)
    response_texts['POST']=response.text
    print("post response :"+response.text)
    # extracting response status_code
    statuscode = response.status_code
    response_codes['POST'] = statuscode

@then('I receive valid HTTP response code 201')
def receive_valid_http_response():
    print('Post rep code ;'+str(response_codes['POST']))
    assert response_codes['POST'] is 201
# END POST Scenario


@given('I Set GET devices api endpoint')
def set_get_api_endpoint():
    api_endpoints['GET_URL'] = api_url+service
    print('url :'+api_endpoints['GET_URL'])


#You may also include "And" or "But" as a step - these are renamed by behave to take the name of their preceding step, so:
@when(parsers.cfparse('Send GET HTTP request to {service_name:Char} service',extra_types=dict(Char=str)))
def send_get_http_request(service_name):
    # sending get request and saving response as response object
    print("--------------------------")
    print(api_endpoints['GET_URL'])
    print(headers)
    print("-------------------------------")

    response = requests.get(url=api_endpoints['GET_URL'], headers=headers, verify=False) #https://jsonplaceholder.typicode.com/posts
    DataUtils.last_response = json.loads(response.text)['results']
    # extracting response text
    response_texts['GET']=response.text
    # extracting response status_code
    statuscode = response.status_code
    response_codes['GET'] = statuscode

@then(parsers.cfparse('I receive valid HTTP response code 200 for {request_name:Char}', extra_types=dict(Char=str)))
def receive_valid_http_response_code_200(request_name):

    print('Get rep code for '+request_name+':'+ str(response_codes[request_name]))
    assert response_codes[request_name] is 200

@then(parsers.parse('verify response attributes:\n{one_col_table_w_header}'))
def verify_response_attribute_values_one_column(datatable, one_col_table_w_header):
    expected_table = parse_str_table(one_col_table_w_header)
    jsonResponse=json.loads(response_texts['GET'])
    print(jsonResponse['results'][0])
    for x in expected_table.get_column(0):
        # for y in expected_table.get_column(1):
        print(x)
    #     if not x in jsonResponse['results'][0]: raise Exception('the field:'+ x + ' is not in the response')
    #     exec(y)


@then(parsers.parse('last response should contain:\n{table_with_header}'))
def verify_response_attribute_values_several_columns(datatable, table_with_header):
    expected_table = parse_str_table(table_with_header)
    jsonResponse = json.loads(response_texts['GET'])
    print(jsonResponse['results'][0])
    for x in expected_table.get_column(0):
        for y in expected_table.get_column(1):
            print(x)
            if not x in jsonResponse['results'][0]: raise Exception('the field:' + x + ' is not in the response')
            exec(y)
