import json
import allure 

from antiphishme.src.config import BASE_PATH
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
@allure.sub_suite("All")
class Tests:

    @allure.description("""
    Test endpoint "/verify/all"

    Send correct data.
    """)
    def test_verify_all_good(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/verify/all'
        data = {
            'url': 'example.com'
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {} with URL: {}".format(endpoint, url))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        j = data_to_json(response.data)
        assert_equal(response.status_code, 200, "Check status code")
        field = "result"
        expected_value = "good"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))