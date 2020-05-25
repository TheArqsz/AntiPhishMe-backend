import json
import allure 

from config import (
    BASE_PATH
)
from tests.test_helpers import (
    data_to_json, 
    info, 
    assert_equal, 
    assert_dict_contains_key
)

@allure.epic("Details")
@allure.parent_suite("Functional")
@allure.suite("Details")
@allure.sub_suite("crt.sh")
class Tests:

    @allure.description("""
    Test endpoint "/details/crtsh"

    Send correct data.
    """)
    def test_details_crtsh(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/crtsh'
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
        field = "caid"
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = "registered_at"
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = "subject"
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = "org_name"
        assert_dict_contains_key(j['details']['subject'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = "country"
        assert_dict_contains_key(j['details']['subject'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = "issuer"
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = "common_name"
        assert_dict_contains_key(j['details']['issuer'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = "multi_dns_amount"
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))

    @allure.description("""
    Test endpoint "/details/crtsh"

    Send wrong data and expect error.
    """)
    def test_details_crtsh_wrong_data(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/crtsh'
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