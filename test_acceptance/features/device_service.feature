Feature: device_service

Background:
	Given I set sample REST API url


#Scenario: get all devices
#  Given I Set GET devices api endpoint
#  When Send GET HTTP request to device service
#  Then I receive valid HTTP response code 200 for GET
#  Then last response should contain:
#    | value | expect                                                                             |
#    | id    | assert(DataUtils.last_response[0]['id'] == 'ec7911c1-b0f5-4c43-a7bd-95fe17b80ca6') |

Scenario: Test rabbit MQ messages
#  Given I send a mock message from json file /Users/miguel.vilchez/tfc-poc-pytest-bdd-device-service/test_acceptance/data/rabbit_mq_messages/valid_rabbitmq_message.json in RabbitMQ to routing key custom.test
  Given I send a mock message with {"message":{"id":"518486ac-df5a-4e16-bfb9-238cbf2a9038"}} in RabbitMQ to routing key custom.test
#  Then I check message {"message":{"id":"518486ac-df5a-4e16-bfb9-238cbf2a9038"}} exists in RabbitMQ for routing key custom.test
  Then I check message sent to RabbitMQ for routing key custo.test should contain:
   | value | expect                                                                             |
   | id    | 518486ac-df5a-4e16-bfb9-238cbf2a9038 |