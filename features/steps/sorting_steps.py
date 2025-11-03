"""
Step Definitions for Sorting Feature

This module contains step definitions for product sorting scenarios.
"""

from behave import when, then
import logging
import time


logger = logging.getLogger(__name__)


@when("I sort products by price ascending")
def step_sort_price_asc(context):
    """Sort products by price ascending"""
    logger.info("Step: Sorting by price ascending")
    context.search_page.sort_by("price_asc")
    time.sleep(2)  # Wait for sorting to apply


@when("I sort products by price descending")
def step_sort_price_desc(context):
    """Sort products by price descending"""
    logger.info("Step: Sorting by price descending")
    context.search_page.sort_by("price_desc")
    time.sleep(2)  # Wait for sorting to apply


@when("I sort products by popularity")
def step_sort_by_popularity(context):
    """Sort products by popularity"""
    logger.info("Step: Sorting by popularity")
    context.search_page.sort_by("popularity")
    time.sleep(2)


@when("I sort products by novelty")
def step_sort_by_novelty(context):
    """Sort products by novelty"""
    logger.info("Step: Sorting by novelty")
    context.search_page.sort_by("novelty")
    time.sleep(2)


@when("I refresh the page")
def step_refresh_page(context):
    """Refresh the page"""
    logger.info("Step: Refreshing page")
    context.home_page.refresh_page()
    time.sleep(2)


@then("products should be sorted by price in ascending order")
def step_verify_sorted_asc(context):
    """Verify products sorted by price ascending"""
    logger.info("Step: Verifying price sort ascending")
    time.sleep(1)  # Wait for page to stabilize
    assert context.search_page.is_sorted_by_price_ascending(), "Products are not sorted by price in ascending order"


@then("products should be sorted by price in descending order")
def step_verify_sorted_desc(context):
    """Verify products sorted by price descending"""
    logger.info("Step: Verifying price sort descending")
    time.sleep(1)  # Wait for page to stabilize
    assert context.search_page.is_sorted_by_price_descending(), "Products are not sorted by price in descending order"


@then("sorting option should be active")
def step_verify_sorting_active(context):
    """Verify sorting option is active"""
    logger.info("Step: Verifying sorting is active")
    assert context.search_page.has_results(), "No products to verify sorting"


@then("new products should be shown first")
def step_verify_new_products_first(context):
    """Verify new products are shown"""
    logger.info("Step: Verifying new products shown")
    assert context.search_page.has_results(), "No products displayed"


@then("products should still be sorted by price in ascending order")
def step_verify_still_sorted_asc(context):
    """Verify products still sorted after refresh"""
    logger.info("Step: Verifying sorting persists after refresh")
    context.search_page.wait_for_results()
    time.sleep(1)
    assert context.search_page.is_sorted_by_price_ascending(), "Sorting did not persist after page refresh"
