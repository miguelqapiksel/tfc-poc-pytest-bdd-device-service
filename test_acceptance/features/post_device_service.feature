Feature: post_device_service
Background:
	Given I set sample REST API url


Scenario: post one device in device service
  Given I run post apocalyptic scenario scenario
  Given I Set POST api endpoint
  Then I subscribe to device.create routing key
  When Set request Body using the data:
       |param                    |value                                     |
       | devicetype              | f3093e8a-26a2-44d3-ae1d-f636baff58ac     |
       | name                    | manager.create_random_name()             |
       | management              | 10.10.10.225                             |
       | devicetype              | 6b6d1986-aa6e-4697-8083-189d01d4133f     |
       | confoptionmandatory     | test 1                                   |
       | confoptionnotmandatory  | test 1                                   |
       | confoptionsecret        | test 1                                   |
       | confoptionnoreguex      | test 1                                   |
       | nameofcustommetadata    | value of custom metadata                 |
       | oldid                   | e1bbfed5-8698-4116-b761-b2f3e298dd56     |
       | location                | roof                                     |
  And Send POST HTTP request
  Then I receive valid HTTP response code 201
  Then I check message sent to RabbitMQ for routing key device.create should contain:
    | value                 | expect                           |
    | attributes.objectId   | json.loads(response_texts['POST'])['id']           |
    | attributes.event      | device.create                    |
    | attributes.entity     | device                           |
    | attributes.action     | create                           |
    | attributes.routingKey | device.create                    |

