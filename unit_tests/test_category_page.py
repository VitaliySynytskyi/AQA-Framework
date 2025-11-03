"""
Unit Tests for Category Page

This module contains unit tests for the CategoryPage class.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.category_page import CategoryPage


class TestCategoryPage:
    """Test suite for CategoryPage"""
    
    @pytest.fixture
    def mock_driver(self):
        """Create mock WebDriver"""
        return Mock()
    
    @pytest.fixture
    def category_page(self, mock_driver):
        """Create CategoryPage instance"""
        return CategoryPage(mock_driver)
    
    def test_category_page_initialization(self, category_page):
        """Test CategoryPage initialization"""
        assert category_page.driver is not None
        assert category_page.CATEGORY_TITLE is not None
    
    @patch('pages.category_page.CategoryPage.is_element_visible')
    def test_wait_for_category_load(self, mock_visible, category_page):
        """Test waiting for category to load"""
        mock_visible.return_value = True
        result = category_page.wait_for_category_load()
        assert result is True
    
    @patch('pages.category_page.CategoryPage.get_text')
    def test_get_category_title(self, mock_text, category_page):
        """Test getting category title"""
        mock_text.return_value = "Laptops and Computers"
        result = category_page.get_category_title()
        assert result == "Laptops and Computers"
    
    @patch('pages.category_page.CategoryPage.find_elements')
    def test_get_products_count(self, mock_find, category_page):
        """Test getting products count"""
        mock_find.return_value = [Mock(), Mock(), Mock(), Mock()]
        result = category_page.get_products_count()
        assert result == 4
    
    @patch('pages.category_page.CategoryPage.find_elements')
    def test_get_product_titles(self, mock_find, category_page):
        """Test getting product titles"""
        mock_title1 = Mock()
        mock_title1.text = "Product 1"
        mock_title2 = Mock()
        mock_title2.text = "Product 2"
        mock_find.return_value = [mock_title1, mock_title2]
        
        result = category_page.get_product_titles()
        assert len(result) == 2
        assert "Product 1" in result
    
    @patch('pages.category_page.CategoryPage.find_elements')
    def test_get_subcategories(self, mock_find, category_page):
        """Test getting subcategories"""
        mock_cat1 = Mock()
        mock_cat1.text = "Subcategory 1"
        mock_cat2 = Mock()
        mock_cat2.text = "Subcategory 2"
        mock_find.return_value = [mock_cat1, mock_cat2]
        
        result = category_page.get_subcategories()
        assert len(result) == 2
        assert "Subcategory 1" in result
    
    @patch('pages.category_page.CategoryPage.click')
    def test_select_subcategory(self, mock_click, category_page):
        """Test selecting subcategory"""
        category_page.select_subcategory("Test Subcategory")
        mock_click.assert_called_once()
    
    @patch('pages.category_page.CategoryPage.find_elements')
    def test_get_breadcrumbs(self, mock_find, category_page):
        """Test getting breadcrumbs"""
        mock_bc1 = Mock()
        mock_bc1.text = "Home"
        mock_bc2 = Mock()
        mock_bc2.text = "Electronics"
        mock_find.return_value = [mock_bc1, mock_bc2]
        
        result = category_page.get_breadcrumbs()
        assert len(result) == 2
        assert "Home" in result
    
    @patch('pages.category_page.CategoryPage.find_elements')
    def test_click_product(self, mock_find, category_page):
        """Test clicking product"""
        mock_product = Mock()
        mock_find.return_value = [mock_product]
        
        category_page.click_product(0)
        mock_product.click.assert_called_once()
    
    def test_click_product_invalid_index(self, category_page):
        """Test clicking product with invalid index"""
        with patch('pages.category_page.CategoryPage.find_elements', return_value=[]):
            with pytest.raises(IndexError):
                category_page.click_product(10)
    
    @patch('pages.category_page.CategoryPage.is_element_present')
    @patch('pages.category_page.CategoryPage.click')
    def test_switch_to_grid_view(self, mock_click, mock_present, category_page):
        """Test switching to grid view"""
        mock_present.return_value = True
        category_page.switch_to_grid_view()
        mock_click.assert_called_once()
    
    @patch('pages.category_page.CategoryPage.is_element_present')
    @patch('pages.category_page.CategoryPage.click')
    def test_switch_to_list_view(self, mock_click, mock_present, category_page):
        """Test switching to list view"""
        mock_present.return_value = True
        category_page.switch_to_list_view()
        mock_click.assert_called_once()
    
    @patch('pages.category_page.CategoryPage.is_element_visible')
    @patch('pages.category_page.CategoryPage.click')
    def test_load_more_products(self, mock_click, mock_visible, category_page):
        """Test loading more products"""
        mock_visible.return_value = True
        category_page.load_more_products()
        mock_click.assert_called_once()
    
    @patch('pages.category_page.CategoryPage.is_element_visible')
    def test_load_more_products_no_button(self, mock_visible, category_page):
        """Test load more when button not visible"""
        mock_visible.return_value = False
        category_page.load_more_products()
        # Should not raise error
    
    @patch('pages.category_page.CategoryPage.click')
    def test_sort_products_price_asc(self, mock_click, category_page):
        """Test sorting products by price ascending"""
        category_page.sort_products('price_asc')
        assert mock_click.call_count == 2
    
    @patch('pages.category_page.CategoryPage.click')
    def test_sort_products_popularity(self, mock_click, category_page):
        """Test sorting products by popularity"""
        category_page.sort_products('popularity')
        assert mock_click.call_count == 2
    
    @patch('pages.category_page.CategoryPage.click')
    def test_sort_products_invalid_option(self, mock_click, category_page):
        """Test sorting with invalid option"""
        with pytest.raises(ValueError):
            category_page.sort_products('invalid_sort')
    
    @patch('pages.category_page.CategoryPage.is_element_visible')
    def test_is_category_page_true(self, mock_visible, category_page):
        """Test is_category_page returns True"""
        mock_visible.return_value = True
        result = category_page.is_category_page()
        assert result is True
    
    @patch('pages.category_page.CategoryPage.is_element_visible')
    def test_is_category_page_false(self, mock_visible, category_page):
        """Test is_category_page returns False"""
        mock_visible.return_value = False
        result = category_page.is_category_page()
        assert result is False
    
    def test_category_title_locator(self, category_page):
        """Test category title locator is defined"""
        assert category_page.CATEGORY_TITLE is not None
    
    def test_product_tiles_locator(self, category_page):
        """Test product tiles locator is defined"""
        assert category_page.PRODUCT_TILES is not None
    
    def test_subcategories_locator(self, category_page):
        """Test subcategories locator is defined"""
        assert category_page.SUBCATEGORIES is not None
