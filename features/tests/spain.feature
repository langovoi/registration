# Created by Alex Kardash at 24/07/2021
Feature: Check google.com

  @monitor_spain @retry1
  Scenario: register germany
    When open url: "https://blsspain-russia.com/moscow/apply_for.php"
    Then page spain visa is opened
    Then check if spain error