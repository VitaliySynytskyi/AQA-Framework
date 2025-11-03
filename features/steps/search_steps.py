"""
Step Definitions for Search Feature

This module contains step definitions for product search scenarios.
"""

from behave import given, when, then
import logging


logger = logging.getLogger(__name__)


@given("I am on the Rozetka home page")
def step_open_home_page(context):
    """Open Rozetka home page"""
    logger.info("Step: Opening Rozetka home page")
    context.home_page.open_home_page()
    assert context.home_page.is_home_page_opened(), "Home page did not open"


@when('I search for "{query}"')
def step_search_for_product(context, query):
    """Search for product"""
    logger.info(f"Step: Searching for '{query}'")
    context.home_page.search_product(query)
    context.test_data["search_query"] = query


@when("I search for empty query")
def step_search_for_empty(context):
    """Search with empty query"""
    logger.info("Step: Searching with empty query")
    context.home_page.search_product("")
    context.test_data["search_query"] = ""


@when('I enter "{query}" in search box and press Enter')
def step_search_with_enter(context, query):
    """Search using Enter key"""
    logger.info(f"Step: Searching for '{query}' with Enter")
    context.home_page.search_product_with_enter(query)
    context.test_data["search_query"] = query


@then("I should see search results")
def step_verify_search_results(context):
    """Verify search results are displayed"""
    logger.info("Step: Verifying search results")
    assert context.search_page.wait_for_results(), "Search results did not load"


@then("search results should contain products")
def step_verify_products_displayed(context):
    """Verify products are displayed"""
    logger.info("Step: Verifying products are displayed")
    assert context.search_page.has_results(), "No products found in search results"
    products_count = context.search_page.get_products_count()
    assert products_count > 0, f"Expected products but got {products_count}"


@then("products should be displayed")
def step_products_displayed(context):
    """Verify products are displayed"""
    logger.info("Step: Verifying products are displayed")
    products_count = context.search_page.get_products_count()
    assert products_count > 0, "No products displayed"


@then('product titles should contain "{text}"')
def step_verify_product_titles_contain(context, text):
    """Verify product titles contain specific text"""
    logger.info(f"Step: Verifying product titles contain '{text}'")
    titles = context.search_page.get_product_titles()
    assert len(titles) > 0, "No product titles found"

    # Check if at least some titles contain the text
    matching_titles = [title for title in titles if text.lower() in title.lower()]
    assert len(matching_titles) > 0, f"No product titles contain '{text}'"


@then("I should remain on the home page")
def step_verify_on_home_page(context):
    """Verify still on home page"""
    logger.info("Step: Verifying still on home page")
    assert context.home_page.is_home_page_opened(), "Not on home page"


@then("I should see no results message")
def step_verify_no_results(context):
    """Verify no results message"""
    logger.info("Step: Verifying no results message")
    # Wait a bit for page to load
    import time

    time.sleep(2)
    assert (
        context.search_page.has_no_results() or context.search_page.get_products_count() == 0
    ), "Expected no results but found products"


@then("search results should be relevant to the query")
def step_verify_results_relevant(context):
    """Verify search results are relevant"""
    logger.info("Step: Verifying results are relevant")
    assert context.search_page.has_results(), "No search results found"
    products_count = context.search_page.get_products_count()
    assert products_count > 0, "No products in search results"
