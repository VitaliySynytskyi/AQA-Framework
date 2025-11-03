"""
Unit Tests for Cart Page

This module contains unit tests for the CartPage class.
"""

import pytest
from pathlib import Path
import sys
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.cart_page import CartPage


class TestCartPage:
    """Test suite for CartPage"""

    @pytest.fixture
    def mock_driver(self):
        """Create mock WebDriver"""
        return Mock()

    @pytest.fixture
    def cart_page(self, mock_driver):
        """Create CartPage instance"""
        return CartPage(mock_driver)

    def test_cart_page_initialization(self, cart_page):
        """Test CartPage initialization"""
        assert cart_page.driver is not None
        assert cart_page.CART_ITEMS is not None

    @patch("pages.cart_page.CartPage.is_element_visible")
    def test_wait_for_cart_load_success(self, mock_visible, cart_page):
        """Test waiting for cart to load"""
        mock_visible.return_value = True
        result = cart_page.wait_for_cart_load()
        assert result is True

    @patch("pages.cart_page.CartPage.is_element_visible")
    def test_is_cart_empty_true(self, mock_visible, cart_page):
        """Test cart is empty"""
        mock_visible.return_value = True
        result = cart_page.is_cart_empty()
        assert result is True

    @patch("pages.cart_page.CartPage.is_element_visible")
    def test_is_cart_empty_false(self, mock_visible, cart_page):
        """Test cart is not empty"""
        mock_visible.return_value = False
        result = cart_page.is_cart_empty()
        assert result is False

    @patch("pages.cart_page.CartPage.is_cart_empty")
    def test_get_items_count_empty_cart(self, mock_empty, cart_page):
        """Test getting items count from empty cart"""
        mock_empty.return_value = True
        result = cart_page.get_items_count()
        assert result == 0

    @patch("pages.cart_page.CartPage.is_cart_empty")
    @patch("pages.cart_page.CartPage.find_elements")
    def test_get_items_count_with_items(self, mock_find, mock_empty, cart_page):
        """Test getting items count with items"""
        mock_empty.return_value = False
        mock_find.return_value = [Mock(), Mock()]
        result = cart_page.get_items_count()
        assert result == 2

    @patch("pages.cart_page.CartPage.is_cart_empty")
    @patch("pages.cart_page.CartPage.find_elements")
    def test_get_item_titles(self, mock_find, mock_empty, cart_page):
        """Test getting item titles"""
        mock_empty.return_value = False
        mock_title1 = Mock()
        mock_title1.text = "Product 1"
        mock_title2 = Mock()
        mock_title2.text = "Product 2"
        mock_find.return_value = [mock_title1, mock_title2]

        result = cart_page.get_item_titles()
        assert len(result) == 2
        assert "Product 1" in result

    @patch("pages.cart_page.CartPage.is_cart_empty")
    def test_get_item_titles_empty_cart(self, mock_empty, cart_page):
        """Test getting titles from empty cart"""
        mock_empty.return_value = True
        result = cart_page.get_item_titles()
        assert result == []

    @patch("pages.cart_page.CartPage.is_cart_empty")
    @patch("pages.cart_page.CartPage.find_elements")
    def test_get_item_prices(self, mock_find, mock_empty, cart_page):
        """Test getting item prices"""
        mock_empty.return_value = False
        mock_price1 = Mock()
        mock_price1.text = "5 000 ₴"
        mock_price2 = Mock()
        mock_price2.text = "10 000 ₴"
        mock_find.return_value = [mock_price1, mock_price2]

        result = cart_page.get_item_prices()
        assert len(result) == 2
        assert 5000.0 in result

    @patch("pages.cart_page.CartPage.is_cart_empty")
    @patch("pages.cart_page.CartPage.get_text")
    def test_get_total_price(self, mock_text, mock_empty, cart_page):
        """Test getting total price"""
        mock_empty.return_value = False
        mock_text.return_value = "15 000 ₴"

        result = cart_page.get_total_price()
        assert result == 15000.0

    @patch("pages.cart_page.CartPage.is_cart_empty")
    def test_get_total_price_empty_cart(self, mock_empty, cart_page):
        """Test getting total price from empty cart"""
        mock_empty.return_value = True
        result = cart_page.get_total_price()
        assert result == 0.0

    @patch("pages.cart_page.CartPage.find_elements")
    def test_remove_item(self, mock_find, cart_page):
        """Test removing item from cart"""
        mock_button = Mock()
        mock_find.return_value = [mock_button]

        cart_page.remove_item(0)
        mock_button.click.assert_called_once()

    def test_remove_item_invalid_index(self, cart_page):
        """Test removing item with invalid index"""
        with patch("pages.cart_page.CartPage.find_elements", return_value=[]):
            with pytest.raises(IndexError):
                cart_page.remove_item(5)

    @patch("pages.cart_page.CartPage.is_cart_empty")
    @patch("pages.cart_page.CartPage.remove_item")
    def test_remove_all_items(self, mock_remove, mock_empty, cart_page):
        """Test removing all items"""
        mock_empty.side_effect = [False, False, True]
        cart_page.remove_all_items()
        assert mock_remove.call_count == 2

    @patch("pages.cart_page.CartPage.find_elements")
    def test_increase_item_quantity(self, mock_find, cart_page):
        """Test increasing item quantity"""
        mock_button = Mock()
        mock_find.return_value = [mock_button]

        cart_page.increase_item_quantity(0)
        mock_button.click.assert_called_once()

    @patch("pages.cart_page.CartPage.find_elements")
    def test_decrease_item_quantity(self, mock_find, cart_page):
        """Test decreasing item quantity"""
        mock_button = Mock()
        mock_find.return_value = [mock_button]

        cart_page.decrease_item_quantity(0)
        mock_button.click.assert_called_once()

    @patch("pages.cart_page.CartPage.find_elements")
    def test_set_item_quantity(self, mock_find, cart_page):
        """Test setting item quantity"""
        mock_input = Mock()
        mock_find.return_value = [mock_input]

        cart_page.set_item_quantity(0, 5)
        mock_input.clear.assert_called_once()
        mock_input.send_keys.assert_called_once_with("5")

    @patch("pages.cart_page.CartPage.find_elements")
    def test_get_item_quantity(self, mock_find, cart_page):
        """Test getting item quantity"""
        mock_input = Mock()
        mock_input.get_attribute.return_value = "3"
        mock_find.return_value = [mock_input]

        result = cart_page.get_item_quantity(0)
        assert result == 3

    @patch("pages.cart_page.CartPage.get_item_titles")
    def test_is_item_in_cart_true(self, mock_titles, cart_page):
        """Test checking if item is in cart - True"""
        mock_titles.return_value = ["Product A", "Product B"]
        result = cart_page.is_item_in_cart("Product A")
        assert result is True

    @patch("pages.cart_page.CartPage.get_item_titles")
    def test_is_item_in_cart_false(self, mock_titles, cart_page):
        """Test checking if item is in cart - False"""
        mock_titles.return_value = ["Product A", "Product B"]
        result = cart_page.is_item_in_cart("Product C")
        assert result is False

    @patch("pages.cart_page.CartPage.is_cart_empty")
    @patch("pages.cart_page.CartPage.click")
    def test_proceed_to_checkout(self, mock_click, mock_empty, cart_page):
        """Test proceeding to checkout"""
        mock_empty.return_value = False
        cart_page.proceed_to_checkout()
        mock_click.assert_called_once()

    @patch("pages.cart_page.CartPage.is_cart_empty")
    @patch("pages.cart_page.CartPage.click")
    def test_proceed_to_checkout_empty_cart(self, mock_click, mock_empty, cart_page):
        """Test checkout with empty cart"""
        mock_empty.return_value = True
        cart_page.proceed_to_checkout()
        mock_click.assert_not_called()

    @patch("pages.cart_page.CartPage.is_cart_empty")
    @patch("pages.cart_page.CartPage.click")
    def test_continue_shopping(self, mock_click, mock_empty, cart_page):
        """Test continue shopping"""
        mock_empty.return_value = True
        cart_page.continue_shopping()
        mock_click.assert_called_once()

    @patch("pages.cart_page.CartPage.is_cart_empty")
    @patch("pages.cart_page.CartPage.get_items_count")
    @patch("pages.cart_page.CartPage.get_item_titles")
    @patch("pages.cart_page.CartPage.get_item_prices")
    @patch("pages.cart_page.CartPage.get_total_price")
    def test_get_cart_summary(self, mock_total, mock_prices, mock_titles, mock_count, mock_empty, cart_page):
        """Test getting cart summary"""
        mock_empty.return_value = False
        mock_count.return_value = 2
        mock_titles.return_value = ["Product 1", "Product 2"]
        mock_prices.return_value = [100.0, 200.0]
        mock_total.return_value = 300.0

        result = cart_page.get_cart_summary()

        assert result["is_empty"] is False
        assert result["items_count"] == 2
        assert len(result["titles"]) == 2
        assert result["total_price"] == 300.0
