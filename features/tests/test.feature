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
    When click on "appointment button"
    When click on "available time button"
    # fill form
    When fill form