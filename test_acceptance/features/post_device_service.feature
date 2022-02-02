Feature: post_device_service
Background:
	Given I initialize REST API main params


Scenario: post one device in device service
  Given I run post apocalyptic scenario scenario
  Given I Set POST api endpoint
  When Set request Body from device_template.json using the data:
    | param                  | value                                        |
    | name                   | manager.create_random_name()                 |
    | management             | manager.create_random_ipv4()                 |
    | devicetype             | 9aefedf0-2573-11e9-8346-139ab5900c6e         |
    | confoptionmandatory    | test 1                                       |
    | confoptionnotmandatory | test 1                                       |
    | confoptionsecret       | test 1                                       |
    | confoptionnoreguex     | test 1                                       |
    | configuration_template | manager.create_random_configuration_option() |
    | first_audio_mc_primary | manager.create_random_mc_value()             |
    | first_meta_mc_primary  | manager.create_random_mc_value()             |
    | first_video_mc_primary | manager.create_random_mc_value()             |
    | io_module_in           | manager.create_random_io_value()             |
    | io_module_out          | manager.create_random_io_value()             |
    | nameofcustommetadata   | value of custom metadata                     |
    | oldid                  | e1bbfed5-8698-4116-b761-b2f3e298dd56         |
    | location               | roof                                         |
  And Send POST HTTP request
  And I send a GET HTTP request by id to the device service
  Then last response should contain:
    | value | expect                                                                                                |
    | id    | assert(json.loads(DataUtils.last_response['GET'])['id'] == json.loads(response_texts['POST'])['id'] ) |
  And I check that the new device created is stored in database
  Then I receive valid HTTP response code 201
  Then I check message sent to RabbitMQ for routing key device.create should contain:
    | value                 | expect                                      |
    | attributes.objectId   | json.loads(response_texts['POST'])['id']    |
    | attributes.event      | device.create                               |
    | attributes.entity     | device                                      |
    | attributes.action     | create                                      |
    | attributes.routingKey | device.create                               |

