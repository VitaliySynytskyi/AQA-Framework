"""
Behave Environment Configuration

This module configures the test environment for Behave BDD tests.
"""

from behave import fixture, use_fixture
import logging
from pathlib import Path

from framework.browser_manager import BrowserManager
from framework.logger import setup_logger
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from pages.category_page import CategoryPage


logger = logging.getLogger(__name__)


@fixture
def browser_fixture(context):
    """Browser fixture to manage browser lifecycle"""
    logger.info("Starting browser fixture")
    context.browser_manager = BrowserManager()
    context.driver = context.browser_manager.start_browser()

    # Initialize page objects
    context.home_page = HomePage(context.driver)
    context.search_page = SearchPage(context.driver)
    context.cart_page = CartPage(context.driver)
    context.category_page = CategoryPage(context.driver)

    # Context storage for test data
    context.test_data = {}

    yield context.driver

    logger.info("Tearing down browser fixture")
    context.browser_manager.quit_browser()


def before_all(context):
    """
    Runs once before all tests

    Args:
        context: Behave context
    """
    logger.info("=" * 80)
    logger.info("STARTING TEST SUITE")
    logger.info("=" * 80)

    # Set up logging
    context.logger = setup_logger("BDD_Tests")

    # Create directories for artifacts
    screenshots_dir = Path(__file__).parent / "screenshots"
    screenshots_dir.mkdir(exist_ok=True)

    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)


def before_feature(context, feature):
    """
    Runs before each feature

    Args:
        context: Behave context
        feature: Feature being executed
    """
    logger.info(f"\n{'=' * 80}")
    logger.info(f"FEATURE: {feature.name}")
    logger.info(f"{'=' * 80}")


def before_scenario(context, scenario):
    """
    Runs before each scenario

    Args:
        context: Behave context
        scenario: Scenario being executed
    """
    logger.info(f"\n{'-' * 80}")
    logger.info(f"SCENARIO: {scenario.name}")
    logger.info(f"{'-' * 80}")

    # Start browser for each scenario
    use_fixture(browser_fixture, context)


def after_scenario(context, scenario):
    """
    Runs after each scenario

    Args:
        context: Behave context
        scenario: Scenario that was executed
    """
    # Take screenshot on failure
    if scenario.status == "failed":
        logger.error(f"Scenario FAILED: {scenario.name}")
        if hasattr(context, "driver") and context.driver:
            screenshot_name = f"failed_{scenario.name.replace(' ', '_')}"
            context.home_page.take_screenshot(screenshot_name)
    else:
        logger.info(f"Scenario PASSED: {scenario.name}")

    logger.info(f"{'-' * 80}\n")


def after_feature(context, feature):
    """
    Runs after each feature

    Args:
        context: Behave context
        feature: Feature that was executed
    """
    logger.info(f"\n{'=' * 80}")
    logger.info(f"COMPLETED FEATURE: {feature.name}")
    logger.info(f"Status: {feature.status}")
    logger.info(f"{'=' * 80}\n")


def after_all(context):
    """
    Runs once after all tests

    Args:
        context: Behave context
    """
    logger.info("\n" + "=" * 80)
    logger.info("TEST SUITE COMPLETED")
    logger.info("=" * 80)
