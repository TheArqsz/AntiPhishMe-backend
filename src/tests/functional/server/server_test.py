import json
import connexion
import pytest
import allure

from config import (
    connexion_app, 
    BASE_PATH, 
    SWAGGER_DIR, 
    arguments, 
    AUTH_API_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS
)
from tests.test_helpers import (
    data_to_json, 
    info, 
    assert_equal, 
    assert_dict_contains_key
)
from flask_sqlalchemy import SQLAlchemy


@allure.epic("Server")
@allure.parent_suite("Functional")
@allure.suite("Server")
#@allure.sub_suite("sub suite name")
class Tests:

    @allure.description("""
    Test endpoint "/server/health"
    """)
    def test_server_health(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/server/create_db'
        headers = {
            "X-API-Key": AUTH_API_KEY
        }
        info("GET {}".format(endpoint))
        response = client.get(BASE_PATH + endpoint, headers=headers)
        assert_equal(response.status_code, 200, "Check status code")
        endpoint = '/server/health'
        info("GET {}".format(endpoint))
        response = client.get(BASE_PATH + endpoint)
        assert_equal(response.status_code, 200, "Check status code")
        j = data_to_json(response.data)
        field = "db_status"
        expected_value = "OK"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        field = "server_status"
        expected_value = "OK"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))

    @allure.description("""
    Test endpoint "/server/create_db" with basic auth
    """)
    def test_database_creation(self, client_with_db):
        client = client_with_db[0]
        endpoint = '/server/create_db'
        headers = {
            "X-API-Key": AUTH_API_KEY
        }
        info("GET {}".format(endpoint))
        response = client.get(BASE_PATH + endpoint, headers=headers)
        assert_equal(response.status_code, 200, "Check status code")
        j = data_to_json(response.data)
        field = "message"
        expected_value = "Database created."
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))

    @allure.description("""
    Test endpoint "/server/add_keyword" with basic auth
    """)
    def test_add_keyword(self, client_with_db):
        client = client_with_db[0]
        db = client_with_db[1]
        endpoint = '/server/create_db'
        headers = {
            "X-API-Key": AUTH_API_KEY
        }
        info("GET {}".format(endpoint))
        response = client.get(BASE_PATH + endpoint, headers=headers)
        assert_equal(response.status_code, 200, "Check status code")
        endpoint = '/server/add_keyword'
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        data = {
            'keyword': 'keyword1234'
        }
        info("POST {}".format(endpoint))
        response = client.post(BASE_PATH + endpoint, headers=headers, data=data)
        j = data_to_json(response.data)
        assert_equal(response.status_code, 200, "Check status code")
        field = "status"
        expected_value = "OK"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))

    @allure.description("""
    Test endpoint "/server/add_keyword" with basic auth

    Send wrong data and expect error.
    """)
    def test_add_keyword_too_short(self, client_with_db):
        client = client_with_db[0]
        db = client_with_db[1]
        endpoint = '/server/create_db'
        headers = {
            "X-API-Key": AUTH_API_KEY
        }
        info("GET {}".format(endpoint))
        response = client.get(BASE_PATH + endpoint, headers=headers)
        assert_equal(response.status_code, 200, "Check status code")
        endpoint = '/server/add_keyword'
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        data = {
            'keyword': 'key'
        }
        info("POST {}".format(endpoint))
        response = client.post(BASE_PATH + endpoint, headers=headers, data=data)
        j = data_to_json(response.data)
        assert_equal(response.status_code, 400, "Check status code")
        field = "detail"
        expected_value = "Keyword too short - min 4 signs"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        field = "status"
        expected_value = 400
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))
        field = "title"
        expected_value = "Bad Request"
        assert_dict_contains_key(j, field, "Check if dict contains given key - \"{}\"".format(field))
        assert_equal(j[field], expected_value, "Check if item \"{}\" is equal to \"{}\"".format(field, expected_value))