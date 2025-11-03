# language: en

Feature: Shopping Cart
  As a user of Rozetka website
  I want to manage products in my shopping cart
  So that I can purchase items

  Background:
    Given I am on the Rozetka home page

  Scenario: Add product to empty cart
    When I search for "мишка"
    And I add first product to cart
    Then cart should contain 1 item
    And the product should be in the cart

  Scenario: Add multiple products to cart
    When I search for "клавіатура"
    And I add first product to cart
    And I search for "мишка"
    And I add first product to cart
    Then cart should contain 2 items

  Scenario: Remove product from cart
    When I search for "навушники"
    And I add first product to cart
    And I open the cart
    And I remove first item from cart
    Then cart should be empty

  Scenario: Verify product details in cart
    When I search for "ноутбук Lenovo"
    And I remember the first product title
    And I add first product to cart
    And I open the cart
    Then the remembered product should be in cart

  Scenario: Increase product quantity in cart
    When I search for "USB кабель"
    And I add first product to cart
    And I open the cart
    When I increase quantity of first item
    Then item quantity should be 2

  Scenario: Cart counter updates correctly
    When I search for "миша"
    And I add first product to cart
    Then cart counter should show 1 item
    When I add second product to cart
    Then cart counter should show 2 items

  Scenario: Empty cart shows appropriate message
    When I open the cart
    Then I should see empty cart message

  Scenario: Navigate to cart and back to shopping
    When I open the cart
    And cart is empty
    When I click continue shopping
    Then I should be on the home page
