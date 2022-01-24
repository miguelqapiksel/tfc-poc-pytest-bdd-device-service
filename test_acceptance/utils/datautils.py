from dotmap import DotMap

class DataUtils(object):
    last_response = {} #last response GET,DELETE,PUT,POST,PATCH should be add it in here
    responses = {}  #response from services should be added here i.e: responses[resource] = json.loads(response.text)
    resources = {}#response from post in services should be added here i.e: resources[resource] = json.loads(response.text)

    def convert_field_expected_to_dict(expected_field,message):
        return eval ('DotMap(message).%s'%expected_field)


datautils = DataUtils()