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

@allure.epic("details")
@allure.parent_suite("Functional")
@allure.story('Functional')
@allure.suite("details")
@allure.sub_suite("IP by URL")
class Tests:

    @allure.description("""
    Test endpoint "/details/ip_by_url"

    Send correct data.
    """)
    def test_details_ip_by_url(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/ip_by_url'
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
        field = "details"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        field = "country"
        expected_value = 'US'
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j['details'][field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        field = "ip"
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        field = "asn"
        assert_dict_contains_key(j['details'], field, "Check if dict contains given key - \"{}\"".format(field))
        

    @allure.description("""
    Test endpoint "/details/ip_by_url"

    Send wrong data and expect error.
    """)
    def test_details_ip_by_url_wrong_data(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/ip'
        data = {
            'temp': '1.1.1.1'
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {} with URL: {}".format(endpoint, '1.1.1.1'))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        j = data_to_json(response.data)
        assert_equal(response.status_code, 400, "Check status code")
        field = "detail"
        expected_value = "'ip' is a required property"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        field = "title"
        expected_value = "Bad Request"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))

    @allure.description("""
    Test endpoint "/details/ip_by_url"

    Send wrong ip and expect 202.
    """)
    def test_details_ip_by_url_wrong_url(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/details/ip_by_url'
        data = {
            'url': 'hppt://no_url'
        }
        headers = {
            'Content-Type': "application/json"
        }
        info("POST {} with URL: {}".format(endpoint, 'hppt://no_url'))
        response = client.post(BASE_PATH + endpoint, data=json.dumps(data), headers=headers)
        j = data_to_json(response.data)
        assert_equal(response.status_code, 202, "Check status code")
        field = "message"
        expected_value = "Correct request but it returned no data"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))