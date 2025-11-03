"""
Step Definitions for Shopping Cart Feature

This module contains step definitions for shopping cart scenarios.
"""

from behave import when, then
import logging
import time


logger = logging.getLogger(__name__)


@when('I add first product to cart')
def step_add_first_product_to_cart(context):
    """Add first product to cart"""
    logger.info("Step: Adding first product to cart")
    context.search_page.wait_for_results()
    context.search_page.add_product_to_cart(0)
    time.sleep(2)  # Wait for cart update


@when('I add second product to cart')
def step_add_second_product_to_cart(context):
    """Add second product to cart"""
    logger.info("Step: Adding second product to cart")
    context.search_page.add_product_to_cart(1)
    time.sleep(2)  # Wait for cart update


@when('I remember the first product title')
def step_remember_product_title(context):
    """Remember first product title"""
    logger.info("Step: Remembering first product title")
    titles = context.search_page.get_product_titles()
    if titles:
        context.test_data['remembered_product'] = titles[0]
        logger.info(f"Remembered product: {titles[0]}")


@when('I open the cart')
def step_open_cart(context):
    """Open shopping cart"""
    logger.info("Step: Opening cart")
    context.home_page.open_cart()
    time.sleep(2)


@when('I remove first item from cart')
def step_remove_first_item(context):
    """Remove first item from cart"""
    logger.info("Step: Removing first item from cart")
    context.cart_page.remove_item(0)
    time.sleep(2)


@when('I increase quantity of first item')
def step_increase_quantity(context):
    """Increase quantity of first item"""
    logger.info("Step: Increasing quantity of first item")
    context.cart_page.increase_item_quantity(0)
    time.sleep(2)


@when('cart is empty')
def step_verify_cart_empty_condition(context):
    """Verify cart is empty (conditional)"""
    logger.info("Step: Checking if cart is empty")
    if not context.cart_page.is_cart_empty():
        context.cart_page.remove_all_items()


@when('I click continue shopping')
def step_click_continue_shopping(context):
    """Click continue shopping"""
    logger.info("Step: Clicking continue shopping")
    context.cart_page.continue_shopping()


@then('cart should contain {count:d} item')
@then('cart should contain {count:d} items')
def step_verify_cart_items_count(context, count):
    """Verify cart contains specific number of items"""
    logger.info(f"Step: Verifying cart contains {count} items")
    actual_count = context.home_page.get_cart_items_count()
    assert actual_count == count, f"Expected {count} items in cart but got {actual_count}"


@then('the product should be in the cart')
def step_verify_product_in_cart(context):
    """Verify product is in cart"""
    logger.info("Step: Verifying product in cart")
    context.home_page.open_cart()
    time.sleep(2)
    assert not context.cart_page.is_cart_empty(), "Cart is empty, expected product"


@then('cart should be empty')
def step_verify_cart_empty(context):
    """Verify cart is empty"""
    logger.info("Step: Verifying cart is empty")
    assert context.cart_page.is_cart_empty(), "Cart is not empty"


@then('the remembered product should be in cart')
def step_verify_remembered_product_in_cart(context):
    """Verify remembered product is in cart"""
    logger.info("Step: Verifying remembered product in cart")
    remembered_product = context.test_data.get('remembered_product', '')
    assert remembered_product, "No product was remembered"
    
    # Check if product is in cart
    assert context.cart_page.is_item_in_cart(remembered_product), \
        f"Product '{remembered_product}' not found in cart"


@then('item quantity should be {quantity:d}')
def step_verify_item_quantity(context, quantity):
    """Verify item quantity"""
    logger.info(f"Step: Verifying item quantity is {quantity}")
    actual_quantity = context.cart_page.get_item_quantity(0)
    assert actual_quantity == quantity, \
        f"Expected quantity {quantity} but got {actual_quantity}"


@then('cart counter should show {count:d} item')
@then('cart counter should show {count:d} items')
def step_verify_cart_counter(context, count):
    """Verify cart counter shows correct count"""
    logger.info(f"Step: Verifying cart counter shows {count}")
    counter = context.home_page.get_cart_items_count()
    assert counter == count, f"Expected cart counter {count} but got {counter}"


@then('I should see empty cart message')
def step_verify_empty_cart_message(context):
    """Verify empty cart message is displayed"""
    logger.info("Step: Verifying empty cart message")
    assert context.cart_page.is_cart_empty(), "Empty cart message not displayed"
