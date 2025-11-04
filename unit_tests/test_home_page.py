"""
Unit Tests for Home Page

This module contains unit tests for the HomePage class.
"""

import pytest
from pathlib import Path
import sys
from selenium.webdriver.common.by import By
from unittest.mock import Mock, patch, MagicMock

sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.home_page import HomePage


class TestHomePage:
    """Test suite for HomePage"""

    @pytest.fixture
    def mock_driver(self):
        """Create mock WebDriver"""
        driver = Mock()
        driver.get = Mock()
        driver.current_url = "https://rozetka.com.ua"
        return driver

    @pytest.fixture
    def home_page(self, mock_driver):
        """Create HomePage instance"""
        return HomePage(mock_driver)

    def test_home_page_initialization(self, home_page):
        """Test HomePage initialization"""
        assert home_page.driver is not None
        assert home_page.SEARCH_INPUT is not None

    @patch("pages.home_page.HomePage.wait_for_element_visible")
    @patch("pages.home_page.HomePage.open")
    def test_open_home_page(self, mock_open, mock_wait, home_page):
        """Test opening home page"""
        result = home_page.open_home_page()
        mock_open.assert_called_once_with("/")
        mock_wait.assert_called_once_with(home_page.SEARCH_INPUT, timeout=20)
        assert result == home_page

    @patch("pages.home_page.HomePage.search_product_with_enter")
    def test_search_product(self, mock_search_with_enter, home_page):
        """Test searching for product (now uses Enter method)"""
        query = "laptop"
        home_page.search_product(query)

        # search_product now calls search_product_with_enter
        mock_search_with_enter.assert_called_once_with(query)

    @patch("pages.home_page.HomePage.wait_for_element_visible")
    @patch("pages.home_page.HomePage.press_key")
    def test_search_product_with_enter(self, mock_press, mock_wait, home_page):
        """Test searching with Enter key"""
        query = "phone"
        mock_element = MagicMock()
        mock_wait.return_value = mock_element

        home_page.search_product_with_enter(query)

        # Should wait for element visibility, clear it, and press Enter
        mock_wait.assert_called_with(home_page.SEARCH_INPUT, timeout=20)
        mock_element.clear.assert_called_once()
        mock_press.assert_called_once_with(home_page.SEARCH_INPUT, "ENTER")

    @patch("pages.home_page.HomePage.click")
    def test_open_catalog(self, mock_click, home_page):
        """Test opening catalog"""
        home_page.open_catalog()
        mock_click.assert_called_once_with(home_page.CATALOG_BUTTON, timeout=10)

    @patch("pages.home_page.HomePage.is_element_visible")
    def test_is_catalog_opened_true(self, mock_visible, home_page):
        """Test catalog is opened"""
        mock_visible.return_value = True
        result = home_page.is_catalog_opened()
        assert result is True

    @patch("pages.home_page.HomePage.is_element_visible")
    def test_is_catalog_opened_false(self, mock_visible, home_page):
        """Test catalog is not opened"""
        mock_visible.return_value = False
        result = home_page.is_catalog_opened()
        assert result is False

    @patch("pages.home_page.HomePage.open_catalog")
    @patch("pages.home_page.HomePage.find_elements")
    def test_get_main_categories(self, mock_find_elements, mock_open_catalog, home_page):
        """Test getting main categories"""
        mock_cat1 = Mock()
        mock_cat1.text = "Category 1"
        mock_cat2 = Mock()
        mock_cat2.text = "Category 2"
        mock_find_elements.return_value = [mock_cat1, mock_cat2]

        result = home_page.get_main_categories()

        assert len(result) == 2
        assert "Category 1" in result
        assert "Category 2" in result

    @patch("pages.home_page.HomePage.open_catalog")
    @patch("pages.home_page.HomePage.click")
    def test_select_category(self, mock_click, mock_open_catalog, home_page):
        """Test selecting category"""
        category_name = "Laptops"
        home_page.select_category(category_name)

        mock_open_catalog.assert_called_once()
        mock_click.assert_called_once()

    @patch("pages.home_page.HomePage.click")
    def test_change_language_to_uk(self, mock_click, home_page):
        """Test changing language to Ukrainian"""
        home_page.change_language("uk")
        assert mock_click.call_count == 2  # Switcher + language option

    @patch("pages.home_page.HomePage.click")
    def test_change_language_to_ru(self, mock_click, home_page):
        """Test changing language to Russian"""
        home_page.change_language("ru")
        assert mock_click.call_count == 2

    @patch("pages.home_page.HomePage.click")
    def test_change_language_invalid(self, mock_click, home_page):
        """Test changing to invalid language raises error"""
        with pytest.raises(ValueError):
            home_page.change_language("invalid")

    @patch("pages.home_page.HomePage.find_element")
    def test_get_current_language(self, mock_find, home_page):
        """Test getting current language"""
        mock_element = Mock()
        mock_element.text = "UA"
        mock_find.return_value = mock_element

        result = home_page.get_current_language()
        assert result == "ua"

    @patch("pages.home_page.HomePage.click")
    def test_open_cart(self, mock_click, home_page):
        """Test opening cart"""
        home_page.open_cart()
        mock_click.assert_called_once_with(home_page.CART_ICON, timeout=10)

    @patch("pages.home_page.HomePage.is_element_visible")
    @patch("pages.home_page.HomePage.get_text")
    def test_get_cart_items_count_with_items(self, mock_get_text, mock_visible, home_page):
        """Test getting cart items count when items exist"""
        mock_visible.return_value = True
        mock_get_text.return_value = "3"

        result = home_page.get_cart_items_count()
        assert result == 3

    @patch("pages.home_page.HomePage.is_element_visible")
    def test_get_cart_items_count_empty(self, mock_visible, home_page):
        """Test getting cart items count when empty"""
        mock_visible.return_value = False

        result = home_page.get_cart_items_count()
        assert result == 0

    @patch("pages.home_page.HomePage.click")
    def test_click_logo(self, mock_click, home_page):
        """Test clicking logo"""
        home_page.click_logo()
        mock_click.assert_called_once_with(home_page.LOGO)

    @patch("pages.home_page.HomePage.get_current_url")
    def test_is_home_page_opened_true(self, mock_url, home_page):
        """Test is_home_page_opened returns True"""
        mock_url.return_value = "https://rozetka.com.ua"
        result = home_page.is_home_page_opened()
        assert result is True

    @patch("pages.home_page.HomePage.get_current_url")
    def test_is_home_page_opened_false(self, mock_url, home_page):
        """Test is_home_page_opened returns False"""
        mock_url.return_value = "https://other-site.com"
        result = home_page.is_home_page_opened()
        assert result is False

    def test_search_input_locator(self, home_page):
        """Test search input locator is defined"""
        assert home_page.SEARCH_INPUT == (By.NAME, "search")

    def test_logo_locator(self, home_page):
        """Test logo locator is defined"""
        assert home_page.LOGO is not None

    def test_cart_icon_locator(self, home_page):
        """Test cart icon locator is defined"""
        assert home_page.CART_ICON is not None
