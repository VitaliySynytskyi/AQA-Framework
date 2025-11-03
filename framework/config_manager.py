"""
Configuration Manager Module

This module handles loading and managing configuration from YAML files
and environment variables.
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any
from dotenv import load_dotenv


class ConfigManager:
    """Manages configuration loading and access"""

    _instance = None
    _config = None

    def __new__(cls):
        """Singleton pattern to ensure single configuration instance"""
        if cls._instance is None:
            cls._instance = super(ConfigManager, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        """Initialize configuration manager"""
        if self._config is None:
            self._load_config()

    def _load_config(self):
        """Load configuration from YAML and environment variables"""
        # Load environment variables
        load_dotenv()

        # Load YAML configuration
        config_path = Path(__file__).parent.parent / "config" / "config.yaml"
        with open(config_path, "r", encoding="utf-8") as file:
            self._config = yaml.safe_load(file)

        # Override with environment variables if present
        self._override_from_env()

    def _override_from_env(self):
        """Override configuration with environment variables"""
        if os.getenv("BASE_URL"):
            self._config["site"]["base_url"] = os.getenv("BASE_URL")

        if os.getenv("BROWSER"):
            self._config["browser"]["name"] = os.getenv("BROWSER")

        if os.getenv("HEADLESS"):
            self._config["browser"]["headless"] = os.getenv("HEADLESS").lower() == "true"

        if os.getenv("IMPLICIT_WAIT"):
            self._config["browser"]["implicit_wait"] = int(os.getenv("IMPLICIT_WAIT"))

        if os.getenv("PAGE_LOAD_TIMEOUT"):
            self._config["browser"]["page_load_timeout"] = int(os.getenv("PAGE_LOAD_TIMEOUT"))

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value by nested key path

        Args:
            key: Dot-separated path to configuration value (e.g., 'browser.name')
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        keys = key.split(".")
        value = self._config

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default

        return value

    def get_browser_config(self) -> Dict[str, Any]:
        """Get browser configuration"""
        return self._config.get("browser", {})

    def get_site_config(self) -> Dict[str, Any]:
        """Get site configuration"""
        return self._config.get("site", {})

    def get_timeouts(self) -> Dict[str, int]:
        """Get timeout configuration"""
        return self._config.get("timeouts", {})

    def get_base_url(self) -> str:
        """Get base URL"""
        return self._config["site"]["base_url"]

    @property
    def config(self) -> Dict[str, Any]:
        """Get full configuration dictionary"""
        return self._config


# Global configuration instance
config = ConfigManager()
