# Created by Alex Kardash at 24/07/2021
@regression
Feature: Check google.com

  Scenario: search
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

  Scenario: endless monitor
    When monitor


