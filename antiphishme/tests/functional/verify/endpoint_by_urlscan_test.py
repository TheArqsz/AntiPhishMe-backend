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

@allure.epic("Verify")
@allure.parent_suite("Functional")
@allure.story('Functional')
@allure.suite("Verify")
@allure.sub_suite("urlscan.io")
class Tests:

    @allure.description("""
    Test endpoint "/verify/by_urlscan"

    Send correct data.
    """)
    def test_verify_by_urlscan(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/verify/by_urlscan'
        data = {
            'url': 'example.com'
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {}".format(endpoint))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        assert_equal(response.status_code, 200, "Check status code")
        j = data_to_json(response.data)
        field = "status"
        expected_value = "good"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))

    @pytest.mark.skipif(getenv('URLSCAN_API_KEY', None) is  None, reason="URLSCAN_API_KEY env variable must be set")
    @allure.description_html("""
    <h5>Test endpoint "/verify/by_urlscan"</h5>

    <h5>Send correct malicious data.</h5>

    <h4> Skip if env. variable not set</h2>
    """)
    def test_verify_by_urlscan_malicious(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/verify/by_urlscan'
        malicious_url = get_test_phishing_domain()
        data = {
            'url': '{}'.format(malicious_url)
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {}".format(endpoint))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        assert_equal(response.status_code, 200, "Check status code")
        if response.status_code == 202:
            pytest.skip("urlscan.io returned status 202 - url \"{}\" is invalid".format(malicious_url))
        j = data_to_json(response.data)
        field = "status"
        expected_value = "malicious"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        if j[field] == "good":
            pytest.skip("urlscan.io returned malicious domain as good - url \"{}\" is invalid".format(malicious_url))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))

    @allure.description("""
    Test endpoint "/verify/by_urlscan"

    Send wrong data and expect error.
    """)
    def test_verify_by_urlscan_wrong_data(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/verify/by_urlscan'
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