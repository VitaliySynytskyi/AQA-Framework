# language: en

Feature: Language Switching
  As a user of Rozetka website
  I want to change the site language
  So that I can browse the site in my preferred language

  Background:
    Given I am on the Rozetka home page

  Scenario: Switch language to Ukrainian
    When I switch language to "uk"
    Then the site should be displayed in Ukrainian language

  Scenario: Switch language to Russian
    When I switch language to "ru"
    Then the site should be displayed in Russian language

  Scenario: Verify language persists after navigation
    When I switch language to "uk"
    And I navigate to "Ноутбуки та комп'ютери" category
    Then the site should still be in Ukrainian language

  Scenario: Verify language persists after search
    When I switch language to "uk"
    And I search for "телефон"
    Then search results should be displayed in Ukrainian

  Scenario: Toggle between languages
    When I switch language to "uk"
    Then current language should be "uk"
    When I switch language to "ru"
    Then current language should be "ru"
