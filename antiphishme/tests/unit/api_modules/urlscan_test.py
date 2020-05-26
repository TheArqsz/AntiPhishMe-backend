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

from antiphishme.src.api_modules.urlscan import (
    check_apikey, 
    search_newest, 
    search, 
    results, 
    submit,
    summary, 
    ApiKeyException, 
    UrlscanException
)

from json import JSONDecodeError

from time import sleep as wait
from datetime import datetime

from secrets import token_hex
from requests import get

@pytest.fixture(scope="module")
def urlscan_data():
    search_url = "example.com"
    wait(5)
    info("Requested url - {}".format(search_url))
    uid = submit(search_url)
    info("Submited search with id {}".format(uid), pre=True)
    r = results(uid, wait_time=120)
    newest = search_newest(search_url)
    yield search_url, uid, r, newest

@allure.epic("api_modules")
@allure.parent_suite("Unit tests")
@allure.suite("api_modules")
@allure.sub_suite("urlscan")
class Tests:

    @allure.description("""
    Test urlscan api module

    Expect exception if api key not set.
    """)
    def test_api_key_check(self):

        if os.getenv('URLSCAN_API_KEY'):
            assert_no_exception( check_apikey , ApiKeyException, "Check if apikey verification does not throw Exception")
        else:
            assert_exception( check_apikey , ApiKeyException, "Check if apikey verification throws Exception")

    @allure.description("""
    Test urlscan api module

    Expect id returned.
    """)
    def test_submit(self):

        url = "example.com"
        info("Requested url - {}".format(url))
        uid = submit(url)
        info("id returned: {}".format(uid))
        assert_type(uid, str, "Check if proper str is returned")

    @allure.description("""
    Test urlscan api module

    Expect UrlscanException.
    """)
    def test_submit_wrong_url(self):

        url = "ftp://localhost"
        info("Requested url - {}".format(url))
        assert_exception( submit , UrlscanException, "Check if submit with wrong url throws UrlscanException", args=url)

    @allure.description("""
    Test urlscan api module

    Expect UrlscanException.
    """)
    def test_submit_google_url(self):

        url = "google.com"
        info("Requested url - {}".format(url))
        assert_exception( submit , UrlscanException, "Check if submit with google.com throws UrlscanException", args=url)
        
    @allure.description("""
    Test urlscan api module

    Expect not empty results.
    """)
    def test_search(self, urlscan_data):
        url = urlscan_data[0]
        info("Requested URL: {}".format(url))
        r = search(url)
        assert_type(r, list, "Check if returned search data is valid list")
        assert_not_empty(r, "Check if returned search data is not empty")

    @allure.description("""
    Test urlscan api module

    Expect not empty results.
    """)
    def test_search_empty(self):
        url = token_hex(25)
        info("Requested URL: {}".format(url))
        r = search(url)
        assert_none(r,  "Check if returned search data is empty")

    @allure.description("""
    Test urlscan api module

    Expect empty results.
    """)
    def test_search_newest(self, urlscan_data):
        url = urlscan_data[0]
        info("Requested URL: {}".format(url))
        r, date = search_newest(url)
        assert_type(r, dict, "Check if returned search data is valid dict")
        assert_not_empty(r, "Check if returned search data is not empty")
        assert_type(date, datetime, "Check if returned search data is valid datetime object")

    @allure.description("""
    Test urlscan api module

    Expect empty results.
    """)
    def test_search_newest_empty(self):
        url = token_hex(25)
        info("Requested URL: {}".format(url))
        r, date = search_newest(url)
        assert_type(r, dict, "Check if returned search data is valid dict")
        assert_empty(r, "Check if returned search data is empty")
        assert_none(date,  "Check if returned date is None")
    
    @allure.description("""
    Test urlscan api module

    Expect not empty results.
    """)
    def test_results(self, urlscan_data):
        uid = urlscan_data[1]
        info("Requested id: {}".format(uid))
        r = results(uid, wait_time=10)
        assert_type(r, dict, "Check if returned search data is valid dict")
        assert_not_empty(r, "Check if returned search data is not empty")

    @allure.description("""
    Test urlscan api module

    Expect empty results.
    """)
    def test_results_invalid_uid(self):
        uid = token_hex(25)
        info("Requested id: {}".format(uid))
        r = results(uid, wait_time=10)
        assert_none(r, "Check if returned search data is None")

    @allure.description("""
    Test urlscan api module

    Expect dict with results.
    """)
    def test_summary(self, urlscan_data):
        uid = urlscan_data[1]
        result_url = "https://urlscan.io/api/v1/result/{}".format(uid)
        info("GET {}".format(result_url))
        response = get(result_url)
        assert_equal(response.status_code, 200, "Check if response's status code is correct (200)")
        r = summary(response.json())
        assert_type(r, dict, "Check if returned search data is valid dict")
        assert_not_empty(r, "Check if returned search data is not empty")

    @allure.description("""
    Test urlscan api module

    Expect None.
    """)
    def test_summary_invalid_data(self, urlscan_data):
        r = summary(dict())
        assert_none(r, "Check if returned search data is None")

    # @allure.description("""
    # Test urlscan api module

    # Expect UrlscanException.
    # """)
    # def test_lookup_url_exception(self):

    #     url = None
    #     info("Requested empty url")
    #     assert_exception( lookup_url, SafeBrowsingException, "Check if empty url throws Exception", args=url)