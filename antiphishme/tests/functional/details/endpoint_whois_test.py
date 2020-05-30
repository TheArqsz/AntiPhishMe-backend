import json
import allure 
import pytest 

from antiphishme.src.config import (
    BASE_PATH
)
from antiphishme.tests.test_helpers import (
    data_to_json, 
    info, 
    assert_equal, 
    assert_dict_contains_key
)

from os import getenv

@allure.epic("Details")
@allure.parent_suite("Functional")
@allure.story('Functional')
@allure.suite("Details")
@allure.sub_suite("who.is")
class Tests:

    @allure.description("""
    Test endpoint "/details/whois"

    Send correct data.
    """)
    def test_details_whois(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/whois'
        url = 'example.com'
        data = {
            'url': "{}".format(url)
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {} with URL: {}".format(endpoint, url))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        assert_equal(response.status_code, 200, "Check status code")
        j = data_to_json(response.data)
        field = "details"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        field = "registrar"
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'creation_date'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'name'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'org'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = 'country'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))

    @allure.description("""
    Test endpoint "/details/whois"

    Send wrong data and expect error.
    """)
    def test_details_safebrowsing_wrong_data(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/whois'
        data = {
            'temp': 'example.com'
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {} with URL: {}".format(endpoint, 'example.com'))
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

    @allure.description("""
    Test endpoint "/details/whois"

    Send wrong data and expect error.
    """)
    def test_details_safebrowsing_wrong_url(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/whois'
        data = {
            'url': 'o'
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {} with URL: {}".format(endpoint, 'o'))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        j = data_to_json(response.data)
        assert_equal(response.status_code, 202, "Check status code")
        field = "message"
        expected_value = "Correct request but it returned no data"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))