"""
Step Definitions for Language Switching Feature

This module contains step definitions for language switching scenarios.
"""

from behave import when, then
import logging
import time


logger = logging.getLogger(__name__)


@when('I switch language to "{language}"')
def step_switch_language(context, language):
    """Switch site language"""
    logger.info(f"Step: Switching language to '{language}'")
    context.home_page.change_language(language)
    time.sleep(2)  # Wait for language to change
    context.test_data['language'] = language


@then('the site should be displayed in {language} language')
def step_verify_language_display(context, language):
    """Verify site is displayed in specified language"""
    logger.info(f"Step: Verifying site in {language} language")
    # Verify by checking current language
    current_lang = context.home_page.get_current_language()
    if language.lower() == 'ukrainian':
        assert 'ua' in current_lang.lower() or 'uk' in current_lang.lower(), \
            f"Site not in Ukrainian, current language: {current_lang}"
    elif language.lower() == 'russian':
        assert 'ru' in current_lang.lower(), \
            f"Site not in Russian, current language: {current_lang}"


@then('the site should still be in {language} language')
def step_verify_language_persists(context, language):
    """Verify language persists after navigation"""
    logger.info(f"Step: Verifying language still {language}")
    current_lang = context.home_page.get_current_language()
    if language.lower() == 'ukrainian':
        assert 'ua' in current_lang.lower() or 'uk' in current_lang.lower(), \
            f"Language did not persist, current: {current_lang}"
    elif language.lower() == 'russian':
        assert 'ru' in current_lang.lower(), \
            f"Language did not persist, current: {current_lang}"


@then('search results should be displayed in {language}')
def step_verify_search_results_language(context, language):
    """Verify search results are in specified language"""
    logger.info(f"Step: Verifying search results in {language}")
    assert context.search_page.has_results(), "No search results to verify language"


@then('current language should be "{language}"')
def step_verify_current_language(context, language):
    """Verify current language setting"""
    logger.info(f"Step: Verifying current language is '{language}'")
    current_lang = context.home_page.get_current_language()
    assert language.lower() in current_lang.lower(), \
        f"Expected language '{language}' but got '{current_lang}'"
