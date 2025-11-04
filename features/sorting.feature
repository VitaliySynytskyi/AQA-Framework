# language: en

Feature: Product Sorting
  As a user of Rozetka website
  I want to sort products by different criteria
  So that I can find products that match my preferences

  Background:
    Given I am on the Rozetka home page
    When I search for "навушники"
    Then I should see search results

  Scenario: Sort products by price from low to high
    When I sort products by price ascending
    Then products should be sorted by price in ascending order

  Scenario: Sort products by price from high to low
    When I sort products by price descending
    Then products should be sorted by price in descending order

  Scenario: Sort products by rating
    When I sort products by rating
    Then products should be displayed
    And sorting option should be active

  Scenario: Sort products by novelty
    When I sort products by novelty
    Then products should be displayed
    And new products should be shown first

  Scenario: Verify price sorting maintains after page refresh
    When I sort products by price ascending
    And I refresh the page
    Then products should still be sorted by price in ascending order
