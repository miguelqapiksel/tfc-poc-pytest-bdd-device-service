Feature: device_service

  Background:
    Given I initialize REST API main params

 # @focus
  Scenario: get all devices
    Given I run get all devices scenario
    Given I Set GET devices api endpoint
    When Send GET HTTP request to device service
    Then I receive valid HTTP response code 200 for GET
  #  Then last response should contain:
  #    | value | expect                               |
  #    | id    | 0ba489b0-5f12-4104-9bbd-4f6e53930e8c |

  Scenario: Test rabbit MQ messages
    Given I send a mock message from json file test_acceptance/data/rabbit_mq_messages/valid_rabbitmq_message.json in RabbitMQ to routing key custom.test
    Given I send a mock message with {"message":{"id":"518486ac-df5a-4e16-bfb9-238cbf2a9038","test":"gramola"},"state":"SUCCESS"} in RabbitMQ to routing key custom.test
  #Then I check message {"message":{"id":"518486ac-df5a-4e16-bfb9-238cbf2a9038"}} exists in RabbitMQ for routing key custom.test
    Then I check message sent to RabbitMQ for routing key custom.test should contain:
      | value        | expect                               |
      | message.id   | 518486ac-df5a-4e16-bfb9-238cbf2a9038 |
      | message.test | gramola                              |
      | state        | SUCCESS                              |

