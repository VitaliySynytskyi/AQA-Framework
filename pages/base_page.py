"""
Base Page Module

This module provides the base page class with common methods for all page objects.
"""

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from typing import List, Optional, Tuple
import logging
from pathlib import Path
from datetime import datetime

from framework.config_manager import config


logger = logging.getLogger(__name__)


class BasePage:
    """Base page class with common methods for all pages"""

    def __init__(self, driver):
        """
        Initialize base page

        Args:
            driver: WebDriver instance
        """
        self.driver = driver
        self.timeouts = config.get_timeouts()
        self.base_url = config.get_base_url()
        self.wait = WebDriverWait(driver, self.timeouts.get("medium", 10))

    def open(self, url: str = ""):
        """
        Open URL in browser

        Args:
            url: URL to open (if empty, opens base_url)
        """
        full_url = url if url.startswith("http") else f"{self.base_url}{url}"
        logger.info(f"Opening URL: {full_url}")
        self.driver.get(full_url)

    def find_element(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        Find element with explicit wait

        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds

        Returns:
            WebElement if found
        """
        wait_time = timeout or self.timeouts.get("medium", 10)
        try:
            element = WebDriverWait(self.driver, wait_time).until(EC.presence_of_element_located(locator))
            logger.debug(f"Found element: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not found: {locator}")
            raise

    def find_elements(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> List:
        """
        Find multiple elements with explicit wait

        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds

        Returns:
            List of WebElements
        """
        wait_time = timeout or self.timeouts.get("medium", 10)
        try:
            elements = WebDriverWait(self.driver, wait_time).until(EC.presence_of_all_elements_located(locator))
            logger.debug(f"Found {len(elements)} elements: {locator}")
            return elements
        except TimeoutException:
            logger.warning(f"No elements found: {locator}")
            return []

    def wait_for_element_visible(
        self, locator: Tuple[str, str], timeout: Optional[int] = None
    ):
        """
        Wait for element to be visible (present + displayed)

        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds

        Returns:
            WebElement when visible
        """
        wait_time = timeout or self.timeouts.get("medium", 10)
        try:
            element = WebDriverWait(self.driver, wait_time).until(
                EC.visibility_of_element_located(locator)
            )
            logger.debug(f"Element visible: {locator}")
            return element
        except TimeoutException:
            logger.error(f"Element not visible: {locator}")
            raise

    def click(self, locator: Tuple[str, str], timeout: Optional[int] = None):
        """
        Click on element with explicit wait

        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds
        """
        wait_time = timeout or self.timeouts.get("medium", 10)
        element = WebDriverWait(self.driver, wait_time).until(EC.element_to_be_clickable(locator))
        logger.debug(f"Clicking element: {locator}")
        element.click()

    def input_text(self, locator: Tuple[str, str], text: str, clear_first: bool = True):
        """
        Input text into element

        Args:
            locator: Tuple of (By strategy, locator value)
            text: Text to input
            clear_first: Whether to clear field before input
        """
        element = self.find_element(locator)
        if clear_first:
            element.clear()
        logger.debug(f"Inputting text '{text}' into: {locator}")
        element.send_keys(text)

    def get_text(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> str:
        """
        Get text from element

        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds

        Returns:
            Element text
        """
        element = self.find_element(locator, timeout)
        text = element.text
        logger.debug(f"Got text '{text}' from: {locator}")
        return text

    def get_attribute(self, locator: Tuple[str, str], attribute: str) -> str:
        """
        Get attribute value from element

        Args:
            locator: Tuple of (By strategy, locator value)
            attribute: Attribute name

        Returns:
            Attribute value
        """
        element = self.find_element(locator)
        value = element.get_attribute(attribute)
        logger.debug(f"Got attribute '{attribute}'='{value}' from: {locator}")
        return value

    def is_element_visible(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        Check if element is visible

        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds

        Returns:
            True if visible, False otherwise
        """
        wait_time = timeout or self.timeouts.get("short", 5)
        try:
            WebDriverWait(self.driver, wait_time).until(EC.visibility_of_element_located(locator))
            logger.debug(f"Element is visible: {locator}")
            return True
        except TimeoutException:
            logger.debug(f"Element is not visible: {locator}")
            return False

    def is_element_present(self, locator: Tuple[str, str]) -> bool:
        """
        Check if element is present in DOM

        Args:
            locator: Tuple of (By strategy, locator value)

        Returns:
            True if present, False otherwise
        """
        try:
            self.driver.find_element(*locator)
            return True
        except NoSuchElementException:
            return False

    def wait_for_element_to_disappear(self, locator: Tuple[str, str], timeout: Optional[int] = None) -> bool:
        """
        Wait for element to disappear

        Args:
            locator: Tuple of (By strategy, locator value)
            timeout: Custom timeout in seconds

        Returns:
            True if disappeared, False otherwise
        """
        wait_time = timeout or self.timeouts.get("medium", 10)
        try:
            WebDriverWait(self.driver, wait_time).until(EC.invisibility_of_element_located(locator))
            logger.debug(f"Element disappeared: {locator}")
            return True
        except TimeoutException:
            logger.warning(f"Element did not disappear: {locator}")
            return False

    def scroll_to_element(self, locator: Tuple[str, str]):
        """
        Scroll to element

        Args:
            locator: Tuple of (By strategy, locator value)
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        logger.debug(f"Scrolled to element: {locator}")

    def hover_over_element(self, locator: Tuple[str, str]):
        """
        Hover mouse over element

        Args:
            locator: Tuple of (By strategy, locator value)
        """
        element = self.find_element(locator)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()
        logger.debug(f"Hovered over element: {locator}")

    def press_key(self, locator: Tuple[str, str], key: str):
        """
        Press keyboard key on element

        Args:
            locator: Tuple of (By strategy, locator value)
            key: Key to press (e.g., Keys.ENTER)
        """
        element = self.find_element(locator)
        element.send_keys(getattr(Keys, key.upper()))
        logger.debug(f"Pressed {key} on element: {locator}")

    def get_current_url(self) -> str:
        """Get current page URL"""
        return self.driver.current_url

    def get_page_title(self) -> str:
        """Get current page title"""
        return self.driver.title

    def refresh_page(self):
        """Refresh current page"""
        logger.info("Refreshing page")
        self.driver.refresh()

    def take_screenshot(self, name: str = "screenshot") -> str:
        """
        Take screenshot of current page

        Args:
            name: Screenshot name

        Returns:
            Path to screenshot file
        """
        screenshot_dir = Path(__file__).parent.parent / "screenshots"
        screenshot_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = screenshot_dir / filename

        self.driver.save_screenshot(str(filepath))
        logger.info(f"Screenshot saved: {filepath}")
        return str(filepath)

    def execute_script(self, script: str, *args):
        """
        Execute JavaScript

        Args:
            script: JavaScript code
            *args: Arguments for script

        Returns:
            Script result
        """
        return self.driver.execute_script(script, *args)

    def switch_to_frame(self, locator: Tuple[str, str]):
        """
        Switch to iframe

        Args:
            locator: Tuple of (By strategy, locator value)
        """
        frame = self.find_element(locator)
        self.driver.switch_to.frame(frame)
        logger.debug(f"Switched to frame: {locator}")

    def switch_to_default_content(self):
        """Switch back to main content from iframe"""
        self.driver.switch_to.default_content()
        logger.debug("Switched to default content")

    def get_elements_count(self, locator: Tuple[str, str]) -> int:
        """
        Get count of elements matching locator

        Args:
            locator: Tuple of (By strategy, locator value)

        Returns:
            Number of elements
        """
        elements = self.find_elements(locator)
        return len(elements)
