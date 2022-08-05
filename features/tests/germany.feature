# Created by Alex Kardash at 24/07/2021
Feature: Check google.com

  @monitor_germany @retry1000
  Scenario: register germany
    When open url: "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId=375"
    Then page german visa is opened
    When get german dates for "375" category

  @register_family
  Scenario: register family
    When open url: "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=mins&realmId=231&categoryId=375"
    Then page german visa is opened
    When register_family
