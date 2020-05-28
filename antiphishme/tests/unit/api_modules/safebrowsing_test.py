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
    info
)

from antiphishme.src.api_modules.safebrowsing import check_apikey, lookup_url, SafeBrowsingException, ApiKeyException

@allure.epic("api_modules")
@allure.parent_suite("Unit tests")
@allure.suite("api_modules")
@allure.sub_suite("safebroswing")
class Tests:

    @allure.description("""
    Test safebrowsing api module

    Expect exception if api key not set.
    """)
    def test_api_key_check(self):

        if os.getenv('SAFEBROWSING_API_KEY'):
            assert_no_exception( check_apikey , ApiKeyException, "Check if apikey verification does not throw Exception")
        else:
            assert_exception( check_apikey , ApiKeyException, "Check if apikey verification throws Exception")

    @allure.description("""
    Test safebrowsing api module

    Expect not malicious.
    """)
    def test_lookup_url(self):

        url = "google.com"
        info("Requested url - {}".format(url))
        l = lookup_url(url)
        assert_type(l, dict, "Check if proper dict is returned")
        assert_not_empty(l, "Check if response is not empty")
        field = "url"
        expected = url
        assert_dict_contains_key(l, field, "Check if url is in response")
        assert_equal(l[field], expected, "Check if proper url is returned")
        field = "malicious"
        expected = False
        assert_dict_contains_key(l, field, "Check if malicious is in response")
        assert_equal(l[field], expected, "Check if proper status is returned")

    @allure.description("""
    Test safebrowsing api module

    Expect malicious.
    """)
    def test_lookup_url_malicious(self):

        url = 'http://malware.testing.google.test/testing/malware/'
        info("Requested url - {}".format(url))
        l = lookup_url(url)
        assert_type(l, dict, "Check if proper dict is returned")
        assert_not_empty(l, "Check if response is not empty")
        field = "url"
        expected = url
        assert_dict_contains_key(l, field, "Check if url is in response")
        assert_equal(l[field], expected, "Check if proper url is returned")
        field = "malicious"
        expected = True
        assert_dict_contains_key(l, field, "Check if malicious is in response")
        assert_equal(l[field], expected, "Check if proper status is returned")

    @allure.description("""
    Test safebrowsing api module

    Expect SafebrowsingException.
    """)
    def test_lookup_url_exception(self):

        url = None
        info("Requested empty url")
        assert_exception( lookup_url, SafeBrowsingException, "Check if empty url throws Exception", args=url)