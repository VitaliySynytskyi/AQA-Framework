# language: en

Feature: Language Switching
  As a user of Rozetka website
  I want to verify the site language
  So that I can browse the site in Ukrainian

  Background:
    Given I am on the Rozetka home page

  Scenario: Verify default language is Ukrainian
    Then the site should be displayed in Ukrainian language

  Scenario: Switch to Ukrainian language explicitly
    When I switch language to "uk"
    Then the site should be displayed in Ukrainian language

  Scenario: Verify language persists after navigation
    When I switch language to "uk"
    And I navigate to "Ноутбуки" category
    Then the site should still be in Ukrainian language

  Scenario: Verify language persists after search
    When I switch language to "uk"
    And I search for "телефон"
    Then search results should be displayed in Ukrainian

  Scenario: Verify Ukrainian language setting
    When I switch language to "uk"
    Then current language should be "uk"
