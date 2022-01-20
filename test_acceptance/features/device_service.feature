Feature: device_service

Background:
	Given I set sample REST API url


Scenario: get all devices
  Given I Set GET devices api endpoint
  When Send GET HTTP request
  Then I receive valid HTTP response code 200 for GET
  Then verify response attributes:
      | name   |
      | Aslak  |
      | Julien |
      | Matt   |



