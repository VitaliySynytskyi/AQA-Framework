"""
Unit Tests for Base Page

This module contains unit tests for the BasePage class.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

sys.path.insert(0, str(Path(__file__).parent.parent))

from pages.base_page import BasePage


class TestBasePage:
    """Test suite for BasePage"""
    
    @pytest.fixture
    def mock_driver(self):
        """Create mock WebDriver"""
        driver = Mock()
        driver.get = Mock()
        driver.find_element = Mock()
        driver.find_elements = Mock()
        driver.execute_script = Mock()
        driver.save_screenshot = Mock(return_value=True)
        driver.current_url = "https://rozetka.com.ua"
        driver.title = "Test Page"
        driver.refresh = Mock()
        driver.switch_to = Mock()
        return driver
    
    @pytest.fixture
    def base_page(self, mock_driver):
        """Create BasePage instance"""
        return BasePage(mock_driver)
    
    def test_base_page_initialization(self, base_page, mock_driver):
        """Test BasePage initialization"""
        assert base_page.driver == mock_driver
        assert base_page.base_url is not None
        assert base_page.timeouts is not None
    
    def test_open_full_url(self, base_page, mock_driver):
        """Test opening full URL"""
        url = "https://example.com"
        base_page.open(url)
        mock_driver.get.assert_called_once_with(url)
    
    def test_open_relative_url(self, base_page, mock_driver):
        """Test opening relative URL"""
        base_page.open('/catalog')
        expected_url = f"{base_page.base_url}/catalog"
        mock_driver.get.assert_called_once_with(expected_url)
    
    def test_open_empty_url(self, base_page, mock_driver):
        """Test opening empty URL (base_url)"""
        base_page.open('')
        mock_driver.get.assert_called_once_with(base_page.base_url)
    
    @patch('pages.base_page.WebDriverWait')
    def test_find_element_success(self, mock_wait, base_page):
        """Test finding element successfully"""
        mock_element = Mock()
        mock_wait.return_value.until.return_value = mock_element
        
        locator = (By.ID, 'test_id')
        result = base_page.find_element(locator)
        
        assert result == mock_element
    
    @patch('pages.base_page.WebDriverWait')
    def test_find_element_timeout(self, mock_wait, base_page):
        """Test find_element raises TimeoutException"""
        mock_wait.return_value.until.side_effect = TimeoutException()
        
        locator = (By.ID, 'nonexistent')
        with pytest.raises(TimeoutException):
            base_page.find_element(locator)
    
    @patch('pages.base_page.WebDriverWait')
    def test_find_elements_success(self, mock_wait, base_page):
        """Test finding multiple elements"""
        mock_elements = [Mock(), Mock(), Mock()]
        mock_wait.return_value.until.return_value = mock_elements
        
        locator = (By.CLASS_NAME, 'test_class')
        result = base_page.find_elements(locator)
        
        assert len(result) == 3
    
    @patch('pages.base_page.WebDriverWait')
    def test_find_elements_empty(self, mock_wait, base_page):
        """Test finding elements returns empty list"""
        mock_wait.return_value.until.side_effect = TimeoutException()
        
        locator = (By.CLASS_NAME, 'nonexistent')
        result = base_page.find_elements(locator)
        
        assert result == []
    
    @patch('pages.base_page.WebDriverWait')
    def test_click_element(self, mock_wait, base_page):
        """Test clicking element"""
        mock_element = Mock()
        mock_wait.return_value.until.return_value = mock_element
        
        locator = (By.ID, 'button')
        base_page.click(locator)
        
        mock_element.click.assert_called_once()
    
    @patch('pages.base_page.BasePage.find_element')
    def test_input_text_with_clear(self, mock_find, base_page):
        """Test inputting text with clear"""
        mock_element = Mock()
        mock_find.return_value = mock_element
        
        locator = (By.ID, 'input')
        text = "test input"
        base_page.input_text(locator, text, clear_first=True)
        
        mock_element.clear.assert_called_once()
        mock_element.send_keys.assert_called_once_with(text)
    
    @patch('pages.base_page.BasePage.find_element')
    def test_input_text_without_clear(self, mock_find, base_page):
        """Test inputting text without clear"""
        mock_element = Mock()
        mock_find.return_value = mock_element
        
        locator = (By.ID, 'input')
        text = "test input"
        base_page.input_text(locator, text, clear_first=False)
        
        mock_element.clear.assert_not_called()
        mock_element.send_keys.assert_called_once_with(text)
    
    @patch('pages.base_page.BasePage.find_element')
    def test_get_text(self, mock_find, base_page):
        """Test getting element text"""
        mock_element = Mock()
        mock_element.text = "Sample Text"
        mock_find.return_value = mock_element
        
        locator = (By.ID, 'element')
        result = base_page.get_text(locator)
        
        assert result == "Sample Text"
    
    @patch('pages.base_page.BasePage.find_element')
    def test_get_attribute(self, mock_find, base_page):
        """Test getting element attribute"""
        mock_element = Mock()
        mock_element.get_attribute.return_value = "attribute_value"
        mock_find.return_value = mock_element
        
        locator = (By.ID, 'element')
        result = base_page.get_attribute(locator, 'href')
        
        assert result == "attribute_value"
    
    @patch('pages.base_page.WebDriverWait')
    def test_is_element_visible_true(self, mock_wait, base_page):
        """Test element visibility returns True"""
        mock_wait.return_value.until.return_value = True
        
        locator = (By.ID, 'visible_element')
        result = base_page.is_element_visible(locator)
        
        assert result is True
    
    @patch('pages.base_page.WebDriverWait')
    def test_is_element_visible_false(self, mock_wait, base_page):
        """Test element visibility returns False"""
        mock_wait.return_value.until.side_effect = TimeoutException()
        
        locator = (By.ID, 'hidden_element')
        result = base_page.is_element_visible(locator)
        
        assert result is False
    
    def test_is_element_present_true(self, base_page, mock_driver):
        """Test element presence returns True"""
        mock_driver.find_element.return_value = Mock()
        
        locator = (By.ID, 'present_element')
        result = base_page.is_element_present(locator)
        
        assert result is True
    
    def test_is_element_present_false(self, base_page, mock_driver):
        """Test element presence returns False"""
        mock_driver.find_element.side_effect = NoSuchElementException()
        
        locator = (By.ID, 'absent_element')
        result = base_page.is_element_present(locator)
        
        assert result is False
    
    @patch('pages.base_page.BasePage.find_element')
    def test_scroll_to_element(self, mock_find, base_page, mock_driver):
        """Test scrolling to element"""
        mock_element = Mock()
        mock_find.return_value = mock_element
        
        locator = (By.ID, 'element')
        base_page.scroll_to_element(locator)
        
        mock_driver.execute_script.assert_called_once()
    
    def test_get_current_url(self, base_page, mock_driver):
        """Test getting current URL"""
        result = base_page.get_current_url()
        assert result == mock_driver.current_url
    
    def test_get_page_title(self, base_page, mock_driver):
        """Test getting page title"""
        result = base_page.get_page_title()
        assert result == mock_driver.title
    
    def test_refresh_page(self, base_page, mock_driver):
        """Test refreshing page"""
        base_page.refresh_page()
        mock_driver.refresh.assert_called_once()
    
    @patch('pages.base_page.Path')
    def test_take_screenshot(self, mock_path, base_page, mock_driver):
        """Test taking screenshot"""
        mock_driver.save_screenshot.return_value = True
        
        result = base_page.take_screenshot('test_screenshot')
        mock_driver.save_screenshot.assert_called_once()
        assert isinstance(result, str)
    
    def test_execute_script(self, base_page, mock_driver):
        """Test executing JavaScript"""
        script = "return document.title;"
        mock_driver.execute_script.return_value = "Test Title"
        
        result = base_page.execute_script(script)
        mock_driver.execute_script.assert_called_once_with(script)
