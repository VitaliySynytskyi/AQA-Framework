"""
Unit Tests for Search Page

This module contains unit tests for the SearchPage class.
"""

import pytest
from pathlib import Path
import sys
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.search_page import SearchPage


class TestSearchPage:
    """Test suite for SearchPage"""

    @pytest.fixture
    def mock_driver(self):
        """Create mock WebDriver"""
        driver = Mock()
        return driver

    @pytest.fixture
    def search_page(self, mock_driver):
        """Create SearchPage instance"""
        return SearchPage(mock_driver)

    def test_search_page_initialization(self, search_page):
        """Test SearchPage initialization"""
        assert search_page.driver is not None
        assert search_page.PRODUCT_TILES is not None

    @patch("pages.search_page.SearchPage.is_element_visible")
    def test_wait_for_results_success(self, mock_visible, search_page):
        """Test waiting for results successfully"""
        mock_visible.return_value = True
        search_page.driver.current_url = "https://rozetka.com.ua/search/?text=laptop"
        result = search_page.wait_for_results()
        assert result is True

    @patch("pages.search_page.SearchPage.is_element_visible")
    def test_wait_for_results_timeout(self, mock_visible, search_page):
        """Test waiting for results times out"""
        mock_visible.return_value = False
        search_page.driver.current_url = "https://rozetka.com.ua/"
        result = search_page.wait_for_results()
        assert result is False

    @patch("pages.search_page.SearchPage.find_elements")
    def test_get_products_count(self, mock_find, search_page):
        """Test getting products count"""
        mock_find.return_value = [Mock(), Mock(), Mock()]
        result = search_page.get_products_count()
        assert result == 3

    @patch("pages.search_page.SearchPage.find_elements")
    def test_get_products_count_zero(self, mock_find, search_page):
        """Test getting zero products count"""
        mock_find.return_value = []
        result = search_page.get_products_count()
        assert result == 0

    @patch("pages.search_page.SearchPage.find_elements")
    def test_get_product_titles(self, mock_find, search_page):
        """Test getting product titles"""
        mock_title1 = Mock()
        mock_title1.text = "Product 1"
        mock_title2 = Mock()
        mock_title2.text = "Product 2"
        mock_find.return_value = [mock_title1, mock_title2]

        result = search_page.get_product_titles()
        assert len(result) == 2
        assert "Product 1" in result

    @patch("pages.search_page.SearchPage.find_elements")
    def test_get_product_prices(self, mock_find, search_page):
        """Test getting product prices"""
        mock_price1 = Mock()
        mock_price1.text = "10 000 ₴"
        mock_price2 = Mock()
        mock_price2.text = "20 000 ₴"
        mock_find.return_value = [mock_price1, mock_price2]

        result = search_page.get_product_prices()
        assert len(result) == 2
        assert 10000.0 in result
        assert 20000.0 in result

    @patch("pages.search_page.SearchPage.find_elements")
    def test_get_product_prices_invalid_format(self, mock_find, search_page):
        """Test getting prices with invalid format"""
        mock_price = Mock()
        mock_price.text = "Invalid Price"
        mock_find.return_value = [mock_price]

        result = search_page.get_product_prices()
        assert len(result) == 0

    @patch("selenium.webdriver.support.ui.Select")
    @patch("pages.search_page.SearchPage.find_element")
    def test_sort_by_price_asc(self, mock_find, mock_select, search_page):
        """Test sorting by price ascending"""
        mock_element = Mock()
        mock_find.return_value = mock_element
        mock_select_instance = Mock()
        mock_select.return_value = mock_select_instance

        search_page.sort_by("price_asc")

        mock_find.assert_called_once_with(search_page.SORT_DROPDOWN, timeout=15)
        mock_select.assert_called_once_with(mock_element)
        mock_select_instance.select_by_value.assert_called_once_with("cheap")

    @patch("selenium.webdriver.support.ui.Select")
    @patch("pages.search_page.SearchPage.find_element")
    def test_sort_by_price_desc(self, mock_find, mock_select, search_page):
        """Test sorting by price descending"""
        mock_element = Mock()
        mock_find.return_value = mock_element
        mock_select_instance = Mock()
        mock_select.return_value = mock_select_instance

        search_page.sort_by("price_desc")

        mock_find.assert_called_once_with(search_page.SORT_DROPDOWN, timeout=15)
        mock_select.assert_called_once_with(mock_element)
        mock_select_instance.select_by_value.assert_called_once_with("expensive")

    @patch("selenium.webdriver.support.ui.Select")
    @patch("pages.search_page.SearchPage.find_element")
    def test_sort_by_popularity(self, mock_find, mock_select, search_page):
        """Test sorting by popularity"""
        mock_element = Mock()
        mock_find.return_value = mock_element
        mock_select_instance = Mock()
        mock_select.return_value = mock_select_instance

        search_page.sort_by("popularity")

        mock_find.assert_called_once_with(search_page.SORT_DROPDOWN, timeout=15)
        mock_select.assert_called_once_with(mock_element)
        mock_select_instance.select_by_value.assert_called_once_with("popularity")

    def test_sort_by_invalid_option(self, search_page):
        """Test sorting with invalid option raises error"""
        with pytest.raises(ValueError):
            search_page.sort_by("invalid_option")

    @patch("pages.search_page.SearchPage.get_product_prices")
    def test_is_sorted_by_price_ascending_true(self, mock_prices, search_page):
        """Test checking ascending sort - True"""
        mock_prices.return_value = [100.0, 200.0, 300.0]
        result = search_page.is_sorted_by_price_ascending()
        assert result is True

    @patch("pages.search_page.SearchPage.get_product_prices")
    def test_is_sorted_by_price_ascending_false(self, mock_prices, search_page):
        """Test checking ascending sort - False"""
        mock_prices.return_value = [300.0, 200.0, 100.0]
        result = search_page.is_sorted_by_price_ascending()
        assert result is False

    @patch("pages.search_page.SearchPage.get_product_prices")
    def test_is_sorted_by_price_descending_true(self, mock_prices, search_page):
        """Test checking descending sort - True"""
        mock_prices.return_value = [300.0, 200.0, 100.0]
        result = search_page.is_sorted_by_price_descending()
        assert result is True

    @patch("pages.search_page.SearchPage.get_product_prices")
    def test_is_sorted_by_price_descending_false(self, mock_prices, search_page):
        """Test checking descending sort - False"""
        mock_prices.return_value = [100.0, 200.0, 300.0]
        result = search_page.is_sorted_by_price_descending()
        assert result is False

    @patch("pages.search_page.SearchPage.get_products_count")
    def test_has_results_true(self, mock_count, search_page):
        """Test has_results returns True"""
        mock_count.return_value = 10
        result = search_page.has_results()
        assert result is True

    @patch("pages.search_page.SearchPage.get_products_count")
    def test_has_results_false(self, mock_count, search_page):
        """Test has_results returns False"""
        mock_count.return_value = 0
        result = search_page.has_results()
        assert result is False

    @patch("pages.search_page.SearchPage.is_element_visible")
    def test_has_no_results_true(self, mock_visible, search_page):
        """Test has_no_results returns True"""
        mock_visible.return_value = True
        result = search_page.has_no_results()
        assert result is True

    @patch("pages.search_page.SearchPage.get_text")
    def test_get_search_query_text(self, mock_get_text, search_page):
        """Test getting search query text"""
        mock_get_text.return_value = "Searching for: laptop"
        result = search_page.get_search_query_text()
        assert "laptop" in result

    @patch("pages.search_page.SearchPage.find_elements")
    def test_click_product(self, mock_find, search_page):
        """Test clicking on product"""
        mock_product = Mock()
        mock_find.return_value = [mock_product]

        search_page.click_product(0)
        mock_product.click.assert_called_once()

    def test_click_product_invalid_index(self, search_page):
        """Test clicking product with invalid index raises error"""
        with patch("pages.search_page.SearchPage.find_elements", return_value=[]):
            with pytest.raises(IndexError):
                search_page.click_product(5)

    @patch("pages.search_page.SearchPage.scroll_to_element")
    @patch("pages.search_page.SearchPage.find_elements")
    def test_add_product_to_cart(self, mock_find, mock_scroll, search_page):
        """Test adding product to cart"""
        mock_button = Mock()
        mock_find.return_value = [mock_button]

        search_page.add_product_to_cart(0)
        mock_button.click.assert_called_once()

    @patch("pages.search_page.SearchPage.input_text")
    @patch("pages.search_page.SearchPage.click")
    def test_set_price_filter_both_values(self, mock_click, mock_input, search_page):
        """Test setting price filter with both min and max"""
        search_page.set_price_filter(min_price=1000, max_price=5000)
        assert mock_input.call_count == 2
        mock_click.assert_called_once()

    @patch("pages.search_page.SearchPage.input_text")
    @patch("pages.search_page.SearchPage.click")
    def test_set_price_filter_min_only(self, mock_click, mock_input, search_page):
        """Test setting price filter with min only"""
        search_page.set_price_filter(min_price=1000)
        mock_input.assert_called_once()
        mock_click.assert_called_once()

    @patch("pages.search_page.SearchPage.is_element_visible")
    @patch("pages.search_page.SearchPage.click")
    def test_go_to_next_page(self, mock_click, mock_visible, search_page):
        """Test going to next page"""
        mock_visible.return_value = True
        search_page.go_to_next_page()
        mock_click.assert_called_once()

    @patch("pages.search_page.SearchPage.is_element_visible")
    def test_has_pagination_true(self, mock_visible, search_page):
        """Test has_pagination returns True"""
        mock_visible.return_value = True
        result = search_page.has_pagination()
        assert result is True
