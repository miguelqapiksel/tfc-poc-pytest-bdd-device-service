import re
import json
from dotmap import DotMap
commands_allowed = ['json.loads',
                    'manager',
                    'DataUtils',
                    'getMethods'] #This list must contains the commands we want to have controll in our executions

class DataUtils(object):
    last_response = {} #last response GET,DELETE,PUT,POST,PATCH should be add it in here
    responses = {}  #response from services should be added here i.e: responses[resource] = json.loads(response.text)
    rabbit_messages = []
    resources = [] #response from post in services should be added here i.e: resources[resource] = json.loads(response.text)


    def convert_field_expected_to_dict(expected_field,message):
        eval_command = ""
        for split_expected_field in expected_field.split("."):
            eval_command += '.get("%s")'% split_expected_field
        return eval ('DotMap(message)%s' % eval_command)

    def is_a_command(expected_field):
        if re.compile('|'.join(commands_allowed), re.IGNORECASE).search(expected_field) is not None:
            return True

    def convert_request(request):
        if DataUtils.is_a_command(request):
           request_command = request[request.index("*") + 1:request.rindex("*")]
           request = request.replace(request_command, eval(request_command)).replace("*", '')
        return request


    def convert_field_expected_to_dict_last_response(expected_field,message):
        eval_command = ""
        for split_expected_field in expected_field.split("."):
            eval_command += '.get("%s")'% split_expected_field
        return eval ('DotMap(message)%s' % eval_command)

    def return_device_id_from_rabbit_message(body_rabbit_message):
        return body_rabbit_message['message']['attributes']['objectId']

datautils = DataUtils()