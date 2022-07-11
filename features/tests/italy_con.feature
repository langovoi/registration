# Created by Alex Kardash at 24/07/2021
Feature: Check google.com

  @monitor_italy @retry1000
  Scenario: montor germany
    When open url: "https://prenotami.esteri.it/"
    Then page german visa is opened
    When enter "captcha" in captcha field
    When click on continue button
    When clear log
    When gather dates
    When click on next month button
    When gather dates
    When click on next month button
    When send dates
