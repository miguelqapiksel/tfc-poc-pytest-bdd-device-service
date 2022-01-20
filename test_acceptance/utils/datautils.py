class DataUtils(object):
    last_response = {} #last response GET,DELETE,PUT,POST,PATCH should be add it in here
    responses = {}  #response from services should be added here i.e: responses[resource] = json.loads(response.text)
    resources = {}#response from post in services should be added here i.e: resources[resource] = json.loads(response.text)

datautils = DataUtils()