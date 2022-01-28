#TFC-4104 - https://nepgroup.atlassian.net/browse/TFC-4104
Feature: integration_test_device_create_flow

Background:
	Given I initialize REST API main params

#Using deviceType/s which are/is going to trigger a new sendersFlow/receiversFlow
Scenario Outline: Integration E2E test for devices that create a flow
  Given I Set POST api endpoint
  When Set request Body from device_template.json using the data:
    | param                  | value                                        |
    | name                   | manager.create_random_name()                 |
    | management             | manager.create_random_ipv4()                   |
    | devicetype             | <device_type>         |
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
  Then I receive valid HTTP response code 201
  Then I check message sent to RabbitMQ for routing key device.create should contain:
    | value                 | expect                           |
    | attributes.objectId   | DataUtils.get_field_from_last_response('id')           |
    | attributes.event      | device.create                    |
    | attributes.entity     | device                           |
    | attributes.action     | create                           |
    | attributes.routingKey | device.create                    |
  When I Send a GET HTTP request to flow with /devices/*DataUtils.get_field_from_last_response('id')*/flows/<type_flow>?limit=1
  Then last response should not be empty
  Then last response should contain:
    | value         | expect                                                      |
    | device_id     | DataUtils.get_field_from_last_response('device_id')                    |
    | production_id | getMethods.get_conf_value('header_x_production_id_default') |

  Examples:

    #|C100 DMV node|EB22|EB23|Embrionix emFusion|LAWO C100|MuoN|PAM-IP#
    | device_type                          | type_flow|
    | d0e300af-bcb8-4715-becf-d0bf8d87960b | receivers         |
    | 88ea9140-6ff4-11e9-99c8-cbb88253d865 | receivers         |
    | 1e9107fc-b894-43cc-b763-d8addaec6df2 | receivers         |
    | e72fa4c0-388d-11e9-a127-ed0c556c028f | receivers         |
    | 9aefedf0-2573-11e9-8346-139ab5900c6e | senders         |
    | c7e227a8-6322-4967-a02a-e95fce6b3c69 | receivers         |
    | 64d7b682-7366-44ea-9257-293e7fbe2c2e | receivers         |

  #Using LAWO a__madi4 deviceType which is not going to trigger a new Flow
  Scenario: Integration E2E test for device LAWO a__madi4 does not create a flow
  Given I Set POST api endpoint
  When Set request Body from device_template.json using the data:
    | param                  | value                                        |
    | name                   | manager.create_random_name()                 |
    | management             | manager.create_random_ipv4()                   |
    | devicetype             | 3c4b4030-444c-11e9-803e-b19926510b86         |
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
  Then I receive valid HTTP response code 201
  Then I check message sent to RabbitMQ for routing key device.create should contain:
    | value                 | expect                           |
    | attributes.objectId   | DataUtils.get_field_from_last_response('id')           |
  When I Send a GET HTTP request to flow with /devices/*DataUtils.get_field_from_last_response('id')*/flows/senders?limit=1
  Then last response should be empty