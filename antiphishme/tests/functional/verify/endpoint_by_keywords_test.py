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

@allure.epic("verify")
@allure.parent_suite("Functional")
@allure.story('Functional')
@allure.suite("verify")
@allure.sub_suite("Keywords")
class Tests:

    @allure.description("""
    Test endpoint "/verify/by_keywords"

    Send correct data.
    """)
    def test_verify_by_keywords(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/verify/by_keywords'
        data = {
            'url': 'example.com'
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {} with URL: {}".format(endpoint, 'example.com'))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        assert_equal(response.status_code, 200, "Check status code")
        j = data_to_json(response.data)
        field = "status"
        expected_value = "good"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))

    @allure.description("""
    Test endpoint "/verify/by_keywords"

    Send wrong data and expect error.
    """)
    def test_verify_by_keywords_wrong_data(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/verify/by_keywords'
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