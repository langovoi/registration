# Created by Alex Kardash at 24/07/2021
Feature: Check google.com

  @monitor_italy #@retry1000
  Scenario: montor germany
    When open url: "https://prenotami.esteri.it/"
    Then page italy consulate is opened
    Then click on language en link
    Then enter "stelmashuk_vova@mail.ru" in email field
    Then enter "visa2020!" in password field
    Then click on forward button
    Then click on language en link
    When open url: "https://prenotami.esteri.it/Services/Booking/163"
    When click on continue button
    When clear log
    When gather dates
    When click on next month button
    When gather dates
    When click on next month button
    When send dates
