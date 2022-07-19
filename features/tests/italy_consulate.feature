# Created by Alex Kardash at 24/07/2021
Feature: Check google.com

  @monitor_italy @retry1000
  Scenario: monitor italy
    When open url: "https://prenotami.esteri.it/"
    Then page italy consulate is opened
#    Then enter "stelmashuk_vova@mail.ru" in email field
#    Then enter "Visa2020!" in password field
    # нужно в ручную нажать кнопку Login
    When wait element book tab
    When click on book tab
    
    When click on search field
#    When enter "Schengen" in search field
    When click on book study button
    When click on privacy checkbox
    When click on forward button
    When accept alert
    When send italy dates
