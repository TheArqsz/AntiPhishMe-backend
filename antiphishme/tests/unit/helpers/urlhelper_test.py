import allure
from unittest import mock
import pytest

from antiphishme.tests.test_helpers import (
    assert_true,
    assert_equal,
    assert_none,
    assert_type,
    assert_false,
    info
)

from antiphishme.src.helpers import url_helper
from secrets import token_hex

@allure.epic("helpers")
@allure.parent_suite("Unit tests")
@allure.suite("helpers")
@allure.sub_suite("urlhelper")
class Tests:

    @allure.description("""
    Test url_helper helpers module

    Given: http url without query
    Expect properly modified url.
    """)
    def test_url_to_domain_http_without_query(self):

        test_url = "http://example.com"
        expected_url = "example.com"
        info("Requested URL: {}".format(test_url))
        result = url_helper.url_to_domain(test_url)
        assert_type(result, str, "Check if returned result is of correct type")
        assert_equal(result, expected_url, "Check if method returned correct url")

    @allure.description("""
    Test url_helper helpers module

    Given: https url without query
    Expect properly modified url.
    """)
    def test_url_to_domain_https_without_query(self):

        test_url = "https://example.com"
        expected_url = "example.com"
        info("Requested URL: {}".format(test_url))
        result = url_helper.url_to_domain(test_url)
        assert_type(result, str, "Check if returned result is of correct type")
        assert_equal(result, expected_url, "Check if method returned correct url")

    @allure.description("""
    Test url_helper helpers module

    Given: url with query
    Expect properly modified url.
    """)
    def test_url_to_domain_with_query(self):

        test_url = "example.com/?a=1&b=2"
        expected_url = "example.com"
        info("Requested URL: {}".format(test_url))
        result = url_helper.url_to_domain(test_url)
        assert_type(result, str, "Check if returned result is of correct type")
        assert_equal(result, expected_url, "Check if method returned correct url")

    @allure.description("""
    Test url_helper helpers module

    Given: http & https url with query
    Expect properly modified url.
    """)
    def test_url_to_domain_schema_with_query(self):

        test_url = "http://example.com/?a=1&b=2"
        expected_url = "example.com"
        info("Requested URL: {}".format(test_url))
        result = url_helper.url_to_domain(test_url)
        assert_type(result, str, "Check if returned result is of correct type")
        assert_equal(result, expected_url, "Check if method returned correct url")
        test_url = "https://example.com/?a=1&b=2"
        expected_url = "example.com"
        info("Requested URL: {}".format(test_url))
        result = url_helper.url_to_domain(test_url)
        assert_type(result, str, "Check if returned result is of correct type")
        assert_equal(result, expected_url, "Check if method returned correct url")

    @allure.description("""
    Test url_helper helpers module

    Given: domain without query
    Expect properly modified url.
    """)
    def test_url_to_domain_schema_with_query(self):

        test_url = "example.com"
        expected_url = "example.com"
        info("Requested URL: {}".format(test_url))
        result = url_helper.url_to_domain(test_url)
        assert_type(result, str, "Check if returned result is of correct type")
        assert_equal(result, expected_url, "Check if method returned correct url")
