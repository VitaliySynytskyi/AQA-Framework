# language: en

Feature: Category Navigation
  As a user of Rozetka website
  I want to navigate through product categories
  So that I can browse products by category

  Background:
    Given I am on the Rozetka home page

  Scenario: Open catalog menu
    When I open the catalog menu
    Then I should see main categories
    And categories list should not be empty

  Scenario: Navigate to specific category
    When I open the catalog menu
    And I select "Ноутбуки" category
    Then I should be on the category page
    And category title should be displayed

  Scenario: Navigate to Tablets category
    When I open the catalog menu
    And I select "Планшети" category
    Then I should be on the category page
    And category title should be displayed

  Scenario: View all main categories
    When I open the catalog menu
    Then I should see at least 10 main categories

  Scenario: Navigate using breadcrumbs
    When I navigate to "Ноутбуки" category
    And I select a subcategory
    Then breadcrumbs should show navigation path

  Scenario: Return to home from category
    When I navigate to any category
    And I click on Rozetka logo
    Then I should be on the home page
