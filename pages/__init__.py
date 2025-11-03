"""
Pages Package Initialization
"""

from pages.base_page import BasePage
from pages.home_page import HomePage
from pages.search_page import SearchPage
from pages.cart_page import CartPage
from pages.category_page import CategoryPage

__all__ = ['BasePage', 'HomePage', 'SearchPage', 'CartPage', 'CategoryPage']
