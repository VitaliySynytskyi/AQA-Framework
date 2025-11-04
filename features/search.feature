# language: en

Feature: Product Search
  As a user of Rozetka website
  I want to search for products
  So that I can find items I'm interested in

  Background:
    Given I am on the Rozetka home page

  Scenario: Successful product search with valid query
    When I search for "ноутбук"
    Then I should see search results
    And search results should contain products

  Scenario: Search with specific product name
    When I search for "iPhone 15"
    Then I should see search results
    And product titles should contain "iPhone"

  Scenario: Search with empty query
    When I search for empty query
    Then I should remain on the home page

  Scenario: Search using Enter key
    When I enter "Samsung" in search box and press Enter
    Then I should see search results
    And search results should contain products

  Scenario: Search for product in Ukrainian
    When I search for "телефон"
    Then I should see search results
    And products should be displayed

  Scenario: Search for product in English
    When I search for "laptop"
    Then I should see search results
    And products should be displayed

  Scenario: Multiple word search query
    When I search for "ігрова консоль"
    Then I should see search results
    And search results should be relevant to the query
