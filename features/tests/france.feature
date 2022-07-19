# Created by Alex Kardash at 24/07/2021
Feature: Check google.com

  @monitor_germany @retry1
  Scenario: register germany
    When open url: "https://pastel.diplomatie.gouv.fr/rdvinternet/html-4.02.00/frameset/frameset.html?lcid=1&sgid=196&suid=1"
    Then page french visa is opened
    When click on book appointments button
    When accept alert
    When wait 300 sec