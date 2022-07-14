# Created by Alex Kardash at 24/07/2021
Feature: Check google.com

  @monitor_germany @retry1000
  Scenario: register germany
    When open url: "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId=373"
    Then page german visa is opened
    When enter "captcha" in captcha field
    When click on continue button
    When gather germany dates
    # select date and time
    When register germany