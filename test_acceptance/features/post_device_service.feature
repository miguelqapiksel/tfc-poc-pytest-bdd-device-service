Feature: post_device_service

Background:
	Given I set sample REST API url


Scenario: post one device in device service
  Given I Set POST api endpoint
  When Set request Body using the data:
       |param                    |value                                 |
       | name                    | test-device-1234567                  |
       | management              | 10.10.10.221                         |
       | devicetype              | 6b6d1986-aa6e-4697-8083-189d01d4133f |
       | confoptionmandatory     | test 1                               |
       | confoptionnotmandatory  | test 1                               |
       | confoptionsecret        | test 1                               |
       | confoptionnoreguex      | test 1                               |
       | nameofcustommetadata    | value of custom metadata             |
       | oldid                   | e1bbfed5-8698-4116-b761-b2f3e298dd56 |
       | location                | roof                                 |
  And Send POST HTTP request
  Then I receive valid HTTP response code 201

