"""
Browser Manager Module

This module handles browser initialization, configuration, and lifecycle management.
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from typing import Optional
import logging

from framework.config_manager import config


logger = logging.getLogger(__name__)


class BrowserManager:
    """Manages browser instances and configuration"""
    
    def __init__(self):
        """Initialize browser manager"""
        self.driver: Optional[webdriver.Remote] = None
        self.browser_config = config.get_browser_config()
    
    def start_browser(self) -> webdriver.Remote:
        """
        Start browser based on configuration
        
        Returns:
            WebDriver instance
        """
        browser_name = self.browser_config.get('name', 'chrome').lower()
        
        logger.info(f"Starting {browser_name} browser")
        
        if browser_name == 'chrome':
            self.driver = self._start_chrome()
        elif browser_name == 'firefox':
            self.driver = self._start_firefox()
        elif browser_name == 'edge':
            self.driver = self._start_edge()
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        self._configure_driver()
        return self.driver
    
    def _start_chrome(self) -> webdriver.Chrome:
        """Start Chrome browser"""
        options = ChromeOptions()
        
        if self.browser_config.get('headless', False):
            options.add_argument('--headless=new')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Set window size
        window_size = self.browser_config.get('window_size', '1920x1080')
        options.add_argument(f'--window-size={window_size}')
        
        service = ChromeService(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=options)
    
    def _start_firefox(self) -> webdriver.Firefox:
        """Start Firefox browser"""
        options = FirefoxOptions()
        
        if self.browser_config.get('headless', False):
            options.add_argument('--headless')
        
        window_size = self.browser_config.get('window_size', '1920x1080')
        width, height = window_size.split('x')
        options.add_argument(f'--width={width}')
        options.add_argument(f'--height={height}')
        
        service = FirefoxService(GeckoDriverManager().install())
        return webdriver.Firefox(service=service, options=options)
    
    def _start_edge(self) -> webdriver.Edge:
        """Start Edge browser"""
        options = EdgeOptions()
        
        if self.browser_config.get('headless', False):
            options.add_argument('--headless')
        
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        
        window_size = self.browser_config.get('window_size', '1920x1080')
        options.add_argument(f'--window-size={window_size}')
        
        service = EdgeService(EdgeChromiumDriverManager().install())
        return webdriver.Edge(service=service, options=options)
    
    def _configure_driver(self):
        """Configure driver with timeouts and settings"""
        if self.driver:
            implicit_wait = self.browser_config.get('implicit_wait', 10)
            page_load_timeout = self.browser_config.get('page_load_timeout', 30)
            
            self.driver.implicitly_wait(implicit_wait)
            self.driver.set_page_load_timeout(page_load_timeout)
            
            if not self.browser_config.get('headless', False):
                self.driver.maximize_window()
            
            logger.info(f"Driver configured with implicit_wait={implicit_wait}s, page_load_timeout={page_load_timeout}s")
    
    def quit_browser(self):
        """Quit browser and cleanup"""
        if self.driver:
            logger.info("Quitting browser")
            try:
                self.driver.quit()
            except Exception as e:
                logger.error(f"Error quitting browser: {e}")
            finally:
                self.driver = None
    
    def get_driver(self) -> Optional[webdriver.Remote]:
        """Get current driver instance"""
        return self.driver
