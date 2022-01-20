Feature: device_service

Background:
	Given I set sample REST API url


Scenario: get all devices
  Given I Set GET devices api endpoint
  When Send GET HTTP request to device service
  Then I receive valid HTTP response code 200 for GET
  Then last response should contain:
    | value | expect                                                                             |
    | id    | assert(DataUtils.last_response[0]['id'] == 'ec7911c1-b0f5-4c43-a7bd-95fe17b80ca6') |