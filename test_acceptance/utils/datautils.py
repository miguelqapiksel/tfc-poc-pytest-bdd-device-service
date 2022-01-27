import re
import ast
import uuid
from dotmap import DotMap
commands_allowed = ['json.loads','manager.create_random_name()', 'manager.create_random_ipv4()'] #This list must contains the commands we want to have controll in our executions

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

    def is_python_code(expected_code):
        try:
            ast.parse(expected_code)
        except (SyntaxError, NameError):
            return False
        return True

    def is_valid_uuid(value):
        try:
            uuid.UUID(value)
            return True
        except ValueError:
            return False


datautils = DataUtils()