import allure
import pytest
import os

from antiphishme.tests.test_helpers import (
    assert_true,
    assert_equal,
    assert_none,
    assert_type,
    assert_exception,
    assert_no_exception,
    assert_false,
    assert_dict_contains_key,
    assert_not_empty,
    assert_empty,
    info
)

from antiphishme.src.api_modules.whois_module import get_results

from time import sleep as wait
from datetime import datetime

from secrets import token_hex

@allure.epic("api_modules")
@allure.parent_suite("Unit tests")
@allure.story('Unit')
@allure.suite("api_modules")
@allure.sub_suite("who.is")
class Tests:

    @allure.description("""
    Test whois api module

    Expect full results.
    """)
    def test_get_results(self):
        url = "google.com"
        info("Requested url - {}".format(url))
        r = get_results(url)
        info("URL returned: {}".format(r))
        assert_type(r, dict, "Check if proper dict is returned")
        field = "registrar"
        assert_dict_contains_key(r, field, "Check if registrar is present in results")
        field = "creation_date"
        assert_dict_contains_key(r, field, "Check if registrar is present in results")
        field = "name"
        assert_dict_contains_key(r, field, "Check if registrar is present in results")
        field = "org"
        assert_dict_contains_key(r, field, "Check if registrar is present in results")
        field = "country"
        assert_dict_contains_key(r, field, "Check if registrar is present in results")
    
    @allure.description("""
    Test whois api module

    Send valid domain but expect None.
    """)
    def test_get_results_empty_by_valid_domain(self):
        url = "example"
        info("Requested url - {}".format(url))
        r = get_results(url)
        info("URL returned: {}".format(r))
        assert_none(r, "Check if None is returned")

        
    @allure.description("""
    Test whois api module

    Send invalid domain but expect None.
    """)
    def test_get_results_by_invalid_domain(self):
        url = ".com"
        info("Requested url - {}".format(url))
        r = get_results(url)
        info("URL returned: {}".format(r))
        assert_none(r, "Check if None is returned")
