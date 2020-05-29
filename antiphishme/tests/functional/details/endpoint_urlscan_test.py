import json
import allure 
import pytest 

from antiphishme.src.config import (
    BASE_PATH
)
from antiphishme.tests.test_helpers import (
    data_to_json, 
    get_test_phishing_domain,
    info, 
    assert_equal, 
    assert_dict_contains_key
)

from os import getenv

@allure.epic("Details")
@allure.parent_suite("Functional")
@allure.story('Functional')
@allure.suite("Details")
@allure.sub_suite("urlscan.io")
class Tests:

    @pytest.mark.skipif(getenv('URLSCAN_API_KEY', None) is  None, reason="URLSCAN_API_KEY env variable must be set")
    @allure.description("""
    Test endpoint "/details/urlscan"

    Send correct data.
    """)
    def test_details_urlscan(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/urlscan'
        url = 'example.com'
        data = {
            'url': "{}".format(url)
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {}".format(endpoint))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        assert_equal(response.status_code, 200, "Check status code")
        j = data_to_json(response.data)
        field = "details"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        field = "domain"
        expected_value = url
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j['details'][field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        field = 'ip'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'country'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'server'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'webApps'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'no_of_requests'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'ads_blocked'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'https_requests'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'ipv6'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'malicious'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'malicious_requests'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'pointed_domains'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'unique_country_count'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        unique_country_count = j['details']['unique_country_count']
        field = 'unique_countries_connected'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        unique_countries_connected = j['details']['unique_countries_connected']
        assert_equal(unique_country_count, len(unique_countries_connected), "Check if amount of connected countries is equal to length of list of unique countries")


    @pytest.mark.skipif(getenv('URLSCAN_API_KEY', None) is  None, reason="URLSCAN_API_KEY env variable must be set")
    @pytest.mark.flaky(reruns=20, reruns_delay=2)
    @allure.description_html("""
    Test endpoint "/details/urlscan"

    Send correct malicious data.

    <h2> Fail if env. variable not set</h2>
    """)
    def test_details_urlscan_malicious(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/urlscan'
        url = get_test_phishing_domain()
        info("URL sent - {}".format(url))
        data = {
            'url': "{}".format(url)
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {}".format(endpoint))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        # if response.status_code == 202:
        #     pytest.skip("urlscan.io returned status 202 - url \"{}\" is invalid".format(url))
        assert_equal(response.status_code, 200, "Check status code")
        j = data_to_json(response.data)
        field = "details"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        field = "domain"
        expected_value = url
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j['details'][field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        field = 'ip'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'country'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'server'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'webApps'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'no_of_requests'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'ads_blocked'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'https_requests'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'ipv6'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'malicious'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        if j['details'][field] == "good":
            pytest.skip("urlscan.io returned malicious domain as good - url \"{}\" is invalid".format(url))
        field = 'malicious_requests'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'pointed_domains'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'unique_country_count'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        unique_country_count = j['details']['unique_country_count']
        field = 'unique_countries_connected'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        unique_countries_connected = j['details']['unique_countries_connected']
        assert_equal(unique_country_count, len(unique_countries_connected), "Check if amount of connected countries is equal to length of list of unique countries")

    @pytest.mark.skipif(getenv('URLSCAN_API_KEY', None) is  None, reason="URLSCAN_API_KEY env variable must be set")
    @allure.description("""
    Test endpoint "/details/urlscan"

    Send wrong data and expect error.
    """)
    def test_details_urlscan_wrong_data(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/urlscan'
        data = {
            'temp': 'example.com'
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {}".format(endpoint))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        j = data_to_json(response.data)
        assert_equal(response.status_code, 400, "Check status code")
        field = "detail"
        expected_value = "'url' is a required property"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        field = "title"
        expected_value = "Bad Request"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))