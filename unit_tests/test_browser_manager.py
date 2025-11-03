"""
Unit Tests for Browser Manager

This module contains unit tests for the BrowserManager class.
"""

import pytest
from unittest.mock import Mock, MagicMock, patch
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from framework.browser_manager import BrowserManager


class TestBrowserManager:
    """Test suite for BrowserManager"""
    
    @pytest.fixture
    def browser_manager(self):
        """Create BrowserManager instance"""
        return BrowserManager()
    
    @pytest.fixture
    def mock_driver(self):
        """Create mock WebDriver"""
        driver = Mock()
        driver.implicitly_wait = Mock()
        driver.set_page_load_timeout = Mock()
        driver.maximize_window = Mock()
        driver.quit = Mock()
        return driver
    
    def test_browser_manager_initialization(self, browser_manager):
        """Test BrowserManager initialization"""
        assert browser_manager.driver is None
        assert browser_manager.browser_config is not None
    
    @patch('framework.browser_manager.webdriver.Chrome')
    @patch('framework.browser_manager.ChromeDriverManager')
    def test_start_chrome_browser(self, mock_chrome_driver, mock_chrome, browser_manager):
        """Test starting Chrome browser"""
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        mock_chrome_driver.return_value.install.return_value = '/path/to/chromedriver'
        
        result = browser_manager._start_chrome()
        assert result is not None
    
    @patch('framework.browser_manager.webdriver.Firefox')
    @patch('framework.browser_manager.GeckoDriverManager')
    def test_start_firefox_browser(self, mock_gecko_driver, mock_firefox, browser_manager):
        """Test starting Firefox browser"""
        mock_driver = Mock()
        mock_firefox.return_value = mock_driver
        mock_gecko_driver.return_value.install.return_value = '/path/to/geckodriver'
        
        result = browser_manager._start_firefox()
        assert result is not None
    
    @patch('framework.browser_manager.webdriver.Edge')
    @patch('framework.browser_manager.EdgeChromiumDriverManager')
    def test_start_edge_browser(self, mock_edge_driver, mock_edge, browser_manager):
        """Test starting Edge browser"""
        mock_driver = Mock()
        mock_edge.return_value = mock_driver
        mock_edge_driver.return_value.install.return_value = '/path/to/edgedriver'
        
        result = browser_manager._start_edge()
        assert result is not None
    
    def test_configure_driver(self, browser_manager, mock_driver):
        """Test driver configuration"""
        browser_manager.driver = mock_driver
        browser_manager._configure_driver()
        
        mock_driver.implicitly_wait.assert_called_once()
        mock_driver.set_page_load_timeout.assert_called_once()
    
    def test_quit_browser(self, browser_manager, mock_driver):
        """Test quitting browser"""
        browser_manager.driver = mock_driver
        browser_manager.quit_browser()
        
        mock_driver.quit.assert_called_once()
        assert browser_manager.driver is None
    
    def test_quit_browser_handles_exception(self, browser_manager, mock_driver):
        """Test quit_browser handles exceptions gracefully"""
        mock_driver.quit.side_effect = Exception("Driver quit failed")
        browser_manager.driver = mock_driver
        
        browser_manager.quit_browser()
        assert browser_manager.driver is None
    
    def test_get_driver(self, browser_manager, mock_driver):
        """Test getting driver instance"""
        browser_manager.driver = mock_driver
        result = browser_manager.get_driver()
        assert result == mock_driver
    
    def test_get_driver_when_none(self, browser_manager):
        """Test getting driver when it's None"""
        result = browser_manager.get_driver()
        assert result is None
    
    def test_unsupported_browser_raises_error(self, browser_manager):
        """Test that unsupported browser raises ValueError"""
        browser_manager.browser_config['name'] = 'unsupported_browser'
        
        with pytest.raises(ValueError, match="Unsupported browser"):
            browser_manager.start_browser()
    
    @patch('framework.browser_manager.webdriver.Chrome')
    @patch('framework.browser_manager.ChromeDriverManager')
    def test_headless_chrome_options(self, mock_chrome_driver, mock_chrome, browser_manager):
        """Test Chrome headless options"""
        browser_manager.browser_config['headless'] = True
        mock_chrome_driver.return_value.install.return_value = '/path/to/chromedriver'
        
        browser_manager._start_chrome()
        # Verify headless option would be set (check through mock calls)
        assert mock_chrome.called
    
    def test_browser_config_window_size(self, browser_manager):
        """Test window size configuration"""
        window_size = browser_manager.browser_config.get('window_size', '1920x1080')
        assert 'x' in window_size
        parts = window_size.split('x')
        assert len(parts) == 2
    
    def test_browser_config_implicit_wait(self, browser_manager):
        """Test implicit wait configuration"""
        implicit_wait = browser_manager.browser_config.get('implicit_wait', 10)
        assert isinstance(implicit_wait, int)
        assert implicit_wait > 0
    
    def test_browser_config_page_load_timeout(self, browser_manager):
        """Test page load timeout configuration"""
        timeout = browser_manager.browser_config.get('page_load_timeout', 30)
        assert isinstance(timeout, int)
        assert timeout > 0
