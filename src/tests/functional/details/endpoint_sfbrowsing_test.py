import json
import allure 
import pytest 

from config import (
    BASE_PATH
)
from tests.test_helpers import (
    data_to_json, 
    info, 
    assert_equal, 
    assert_dict_contains_key
)

from os import getenv

@allure.epic("Details")
@allure.parent_suite("Functional")
@allure.suite("Details")
@allure.sub_suite("Safebrowsing")
class Tests:

    @pytest.mark.skipif(getenv('SAFEBROWSING_API_KEY', None) is  None, reason="SAFEBROWSING_API_KEY env variable must be set")
    @allure.description("""
    Test endpoint "/details/safebrowsing"

    Send correct data.
    """)
    def test_details_safebrowsing(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/safebrowsing'
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
        field = "url"
        expected_value = url
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j['details'][field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        field = 'malicious'
        expected_value = False
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j['details'][field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))


    @pytest.mark.skipif(getenv('SAFEBROWSING_API_KEY', None) is  None, reason="SAFEBROWSING_API_KEY env variable must be set")
    @allure.description_html("""
    Test endpoint "/details/safebrowsing"

    Send correct malicious data.

    <h2> Fail if env. variable not set</h2>
    """)
    def test_details_safebrowsing_malicious(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/safebrowsing'
        url = 'http://malware.testing.google.test/testing/malware/'
        info("URL sent - {}".format(url))
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
        field = "url"
        expected_value = url
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j['details'][field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        field = 'malicious'
        expected_value = True
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j['details'][field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))

    @pytest.mark.skipif(getenv('SAFEBROWSING_API_KEY', None) is  None, reason="SAFEBROWSING_API_KEY env variable must be set")
    @allure.description("""
    Test endpoint "/details/safebrowsing"

    Send wrong data and expect error.
    """)
    def test_details_safebrowsing_wrong_data(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/safebrowsing'
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