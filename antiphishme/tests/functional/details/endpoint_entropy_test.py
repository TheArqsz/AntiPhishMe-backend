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
@allure.sub_suite("Entropy")
class Tests:

    @allure.description("""
    Test endpoint "/details/entropy"

    Send correct data.
    """)
    def test_details_entropy(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/entropy'
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
        field = "details"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        field = "entropy"
        expected_value = 3.1
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j['details'][field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        

    @allure.description("""
    Test endpoint "/details/entropy"

    Send wrong data and expect error.
    """)
    def test_details_entropy_wrong_data(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/entropy'
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