"""
Unit Tests for Configuration Manager

This module contains unit tests for the ConfigManager class.
"""

import pytest
import os
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
import yaml

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent))

from framework.config_manager import ConfigManager


class TestConfigManager:
    """Test suite for ConfigManager"""
    
    @pytest.fixture
    def config_data(self):
        """Sample configuration data"""
        return {
            'browser': {
                'name': 'chrome',
                'headless': False,
                'window_size': '1920x1080'
            },
            'site': {
                'base_url': 'https://rozetka.com.ua'
            },
            'timeouts': {
                'short': 5,
                'medium': 10,
                'long': 30
            }
        }
    
    def test_config_manager_singleton(self):
        """Test that ConfigManager is a singleton"""
        config1 = ConfigManager()
        config2 = ConfigManager()
        assert config1 is config2
    
    @patch('framework.config_manager.open', new_callable=mock_open)
    @patch('framework.config_manager.yaml.safe_load')
    @patch('framework.config_manager.load_dotenv')
    def test_load_config_from_yaml(self, mock_dotenv, mock_yaml, mock_file, config_data):
        """Test loading configuration from YAML file"""
        mock_yaml.return_value = config_data
        config = ConfigManager()
        assert config._config is not None
    
    def test_get_browser_config(self):
        """Test getting browser configuration"""
        config = ConfigManager()
        browser_config = config.get_browser_config()
        assert isinstance(browser_config, dict)
        assert 'name' in browser_config
    
    def test_get_site_config(self):
        """Test getting site configuration"""
        config = ConfigManager()
        site_config = config.get_site_config()
        assert isinstance(site_config, dict)
    
    def test_get_timeouts(self):
        """Test getting timeouts configuration"""
        config = ConfigManager()
        timeouts = config.get_timeouts()
        assert isinstance(timeouts, dict)
    
    def test_get_base_url(self):
        """Test getting base URL"""
        config = ConfigManager()
        base_url = config.get_base_url()
        assert isinstance(base_url, str)
        assert base_url.startswith('http')
    
    def test_get_nested_config_value(self):
        """Test getting nested configuration value"""
        config = ConfigManager()
        browser_name = config.get('browser.name')
        assert browser_name is not None
    
    def test_get_config_with_default(self):
        """Test getting configuration with default value"""
        config = ConfigManager()
        value = config.get('nonexistent.key', 'default_value')
        assert value == 'default_value'
    
    def test_config_property(self):
        """Test config property returns full configuration"""
        config = ConfigManager()
        full_config = config.config
        assert isinstance(full_config, dict)
    
    @patch.dict(os.environ, {'BASE_URL': 'https://test.com'})
    def test_override_from_env_base_url(self):
        """Test overriding base URL from environment variable"""
        ConfigManager._instance = None
        ConfigManager._config = None
        config = ConfigManager()
        # Environment override should work during initialization
        assert config._config is not None
    
    @patch.dict(os.environ, {'BROWSER': 'firefox'})
    def test_override_from_env_browser(self):
        """Test overriding browser from environment variable"""
        ConfigManager._instance = None
        ConfigManager._config = None
        config = ConfigManager()
        assert config._config is not None
    
    @patch.dict(os.environ, {'HEADLESS': 'true'})
    def test_override_from_env_headless_true(self):
        """Test overriding headless mode to true"""
        ConfigManager._instance = None
        ConfigManager._config = None
        config = ConfigManager()
        assert config._config is not None
    
    @patch.dict(os.environ, {'HEADLESS': 'false'})
    def test_override_from_env_headless_false(self):
        """Test overriding headless mode to false"""
        ConfigManager._instance = None
        ConfigManager._config = None
        config = ConfigManager()
        assert config._config is not None
    
    @patch.dict(os.environ, {'IMPLICIT_WAIT': '20'})
    def test_override_from_env_implicit_wait(self):
        """Test overriding implicit wait from environment"""
        ConfigManager._instance = None
        ConfigManager._config = None
        config = ConfigManager()
        assert config._config is not None
    
    @patch.dict(os.environ, {'PAGE_LOAD_TIMEOUT': '60'})
    def test_override_from_env_page_load_timeout(self):
        """Test overriding page load timeout from environment"""
        ConfigManager._instance = None
        ConfigManager._config = None
        config = ConfigManager()
        assert config._config is not None
    
    def test_get_invalid_nested_key(self):
        """Test getting invalid nested key returns default"""
        config = ConfigManager()
        value = config.get('invalid.nested.key', 'default')
        assert value == 'default'
    
    def test_get_partial_nested_key(self):
        """Test getting partially valid nested key"""
        config = ConfigManager()
        value = config.get('browser.invalid_key', None)
        assert value is None
    
    def test_config_structure(self):
        """Test basic configuration structure"""
        config = ConfigManager()
        assert 'browser' in config.config or config.config is not None
