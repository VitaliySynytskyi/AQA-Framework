"""
Step Definitions for Navigation Feature

This module contains step definitions for category navigation scenarios.
"""

from behave import when, then
import logging


logger = logging.getLogger(__name__)


@when('I open the catalog menu')
def step_open_catalog(context):
    """Open catalog menu"""
    logger.info("Step: Opening catalog menu")
    context.home_page.open_catalog()


@when('I select "{category}" category')
def step_select_category(context, category):
    """Select category from catalog"""
    logger.info(f"Step: Selecting category '{category}'")
    context.home_page.select_category(category)
    context.test_data['selected_category'] = category


@when('I navigate to "{category}" category')
def step_navigate_to_category(context, category):
    """Navigate to specific category"""
    logger.info(f"Step: Navigating to category '{category}'")
    context.home_page.open_catalog()
    context.home_page.select_category(category)


@when('I navigate to any category')
def step_navigate_to_any_category(context):
    """Navigate to any category"""
    logger.info("Step: Navigating to any category")
    context.home_page.open_catalog()
    categories = context.home_page.get_main_categories()
    if categories:
        context.home_page.select_category(categories[0])


@when('I select a subcategory')
def step_select_subcategory(context):
    """Select a subcategory"""
    logger.info("Step: Selecting a subcategory")
    subcategories = context.category_page.get_subcategories()
    if subcategories:
        context.category_page.select_subcategory(subcategories[0])


@when('I click on breadcrumb "{breadcrumb}"')
def step_click_breadcrumb(context, breadcrumb):
    """Click on breadcrumb"""
    logger.info(f"Step: Clicking breadcrumb '{breadcrumb}'")
    breadcrumb_locator = ('xpath', f"//ul[contains(@class, 'breadcrumbs')]//a[contains(text(), '{breadcrumb}')]")
    context.home_page.click(breadcrumb_locator)


@when('I click on Rozetka logo')
def step_click_logo(context):
    """Click on Rozetka logo"""
    logger.info("Step: Clicking Rozetka logo")
    context.home_page.click_logo()


@then('I should see main categories')
def step_verify_main_categories(context):
    """Verify main categories are visible"""
    logger.info("Step: Verifying main categories visible")
    assert context.home_page.is_catalog_opened(), "Catalog menu is not opened"


@then('categories list should not be empty')
def step_verify_categories_not_empty(context):
    """Verify categories list is not empty"""
    logger.info("Step: Verifying categories list not empty")
    categories = context.home_page.get_main_categories()
    assert len(categories) > 0, "Categories list is empty"


@then('I should be on the category page')
def step_verify_on_category_page(context):
    """Verify on category page"""
    logger.info("Step: Verifying on category page")
    assert context.category_page.wait_for_category_load(), "Category page did not load"


@then('category title should be displayed')
def step_verify_category_title(context):
    """Verify category title is displayed"""
    logger.info("Step: Verifying category title displayed")
    title = context.category_page.get_category_title()
    assert title, "Category title is not displayed"


@then('I should see at least {count:d} main categories')
def step_verify_min_categories(context, count):
    """Verify minimum number of categories"""
    logger.info(f"Step: Verifying at least {count} categories")
    categories = context.home_page.get_main_categories()
    assert len(categories) >= count, f"Expected at least {count} categories but got {len(categories)}"


@then('breadcrumbs should show navigation path')
def step_verify_breadcrumbs(context):
    """Verify breadcrumbs show navigation path"""
    logger.info("Step: Verifying breadcrumbs")
    breadcrumbs = context.category_page.get_breadcrumbs()
    assert len(breadcrumbs) > 1, "Breadcrumbs not showing navigation path"


@then('I should return to parent category')
def step_verify_parent_category(context):
    """Verify returned to parent category"""
    logger.info("Step: Verifying returned to parent category")
    assert context.category_page.is_category_page(), "Not on category page"


@then('I should be on the home page')
def step_verify_on_home_page(context):
    """Verify on home page"""
    logger.info("Step: Verifying on home page")
    assert context.home_page.is_home_page_opened(), "Not on home page"
