Feature: device_service

Background:
	Given I set sample REST API url


Scenario: get all devices
  Given I Set GET devices api endpoint
  When Send GET HTTP request
  Then I receive valid HTTP response code 200 for GET
  Then verify response attributes:
      |Attributes             |
      |id                     |
      |name                   |
      |management_ip          |
      |tier_number            |
      |configuration_values   |
      |custom_metadata        |
      |device_monitoring      |
      |delete_origin          |
      |production_id          |
      |created_at             |
      |updated_at             |
      |deleted_at             |
      |_links                 |
      |_embedded              |


