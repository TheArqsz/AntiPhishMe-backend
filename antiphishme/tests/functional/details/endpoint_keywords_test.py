import json
import allure 

from antiphishme.src.config import (
    BASE_PATH
)
from antiphishme.tests.test_helpers import (
    data_to_json, 
    info, 
    assert_equal, 
    assert_dict_contains_key
)

@allure.epic("Details")
@allure.parent_suite("Functional")
@allure.story('Functional')
@allure.suite("Details")
@allure.sub_suite("Keywords")
class Tests:

    @allure.description("""
    Test endpoint "/details/keywords"

    Send correct data.
    """)
    def test_details_keywords(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/keywords'
        data = {
            'url': 'google.com'
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
        field = "matched_keyword"
        expected_value = 'google'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j['details'][field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))

    @allure.description("""
    Test endpoint "/details/keywords"

    Send wrong data and expect error.
    """)
    def test_verify_by_keywords_wrong_data(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/keywords'
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

    @allure.description("""
    Test endpoint "/details/keywords"

    Send wrong url and expect 202.
    """)
    def test_details_keywords_wrong_url(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/keywords'
        data = {
            'url': '.'
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {}".format(endpoint))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        j = data_to_json(response.data)
        assert_equal(response.status_code, 202, "Check status code")
        field = "message"
        expected_value = "Correct request but it returned no data"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))