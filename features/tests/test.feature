# Created by Alex Kardash at 24/07/2021
Feature: Check google.com

  @monitor_germany @retry1000
  Scenario: montor germany
    When open url: "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId=373"
    Then page german visa is opened
    When enter "captcha" in captcha field
    When click on continue button
    When clear log
    When gather dates
    When click on next month button
    When gather dates
    When click on next month button
    When send dates

  @register_germany
  Scenario: register germany
    When open url: "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId=373"
    Then page german visa is opened
    When enter "captcha" in captcha field
    When click on continue button
    # select date and time
    When click on appointment button
    # fill form
    When enter "{surname}" in surname field
    When enter "{name}" in name field
    When enter "{email}" in email field
    When enter "{email}" in confirm email field
    When select "{number_of_applicants}" in "applicants number dropdown"
    When enter "{passport_number}" in passport number field
    When enter "{other_applicants_info}" in other applicants field
    When enter "{aim}" in aim field
    When enter "{phone_number}" in phone number field
    When click on confirm checkbox
    When enter "captcha" in captcha field
    When click on save button
    When click on confirm time link
