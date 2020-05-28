import allure
from unittest import mock
import pytest
import json

from antiphishme.tests.test_helpers import (
    assert_dict_contains_key,
    assert_not_empty,
    assert_equal,
    assert_type,
    assert_exception,
    info
)

from antiphishme.src.api.details import (
    get_ip_details,
    get_ip_details_by_url
)
from secrets import token_hex

from antiphishme.src.config import AUTH_API_KEY
from werkzeug.exceptions import BadRequest
from flask import Response

@allure.epic("api")
@allure.parent_suite("Unit tests")
@allure.suite("api")
@allure.sub_suite("details")
class Tests:

    @allure.description("""
    Test details api module

    Expect correct response.
    """)
    def test_get_ip_details(self):
        ip = "1.1.1.1"
        ip_body = {
            "ip": ip
        }
        info("Requested ip body: {}".format(ip_body))
        resp = get_ip_details(ip_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_equal(resp.status_code, 200, "Check if correct status code was returned")
        json_data = json.loads(resp.data.decode('utf-8'))
        info(json_data)
        assert_type(json_data, dict, "Check if returned result is of correct type")
        assert_not_empty(json_data, "Check if returned dict is not empty")
        field = "details"
        assert_dict_contains_key(json_data, field, "Check if returned dict contains '{}' key".format(field))
        field = "country"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "ip"
        expected = ip
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        assert_equal(json_data['details'][field], expected, "Check if correct status code was returned")
        field = "asn"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))

    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_get_ip_details_bad_ip(self):
        ip = token_hex(6)
        ip_body = {
            "ip": ip
        }
        info("Requested ip body: {}".format(ip_body))
        with allure.step("[STEP] Check if proper exception is raised: {}".format(BadRequest)):
            with pytest.raises(BadRequest, match="Wrong IP"):
                get_ip_details(ip_body)

    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_get_ip_details_bad_body(self):
        ip_body = {
            "tmp": 1
        }
        info("Requested ip body: {}".format(ip_body))
        with allure.step("[STEP] Check if proper exception is raised: {}".format(BadRequest)):
            with pytest.raises(BadRequest, match="'ip' is a required property"):
                get_ip_details(ip_body)

    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_get_ip_details_empty_ip(self):
        ip_body = {
            "ip": ""
        }
        info("Requested ip body: {}".format(ip_body))
        with allure.step("[STEP] Check if proper exception is raised: {}".format(BadRequest)):
            with pytest.raises(BadRequest, match="Wrong IP"):
                get_ip_details(ip_body)

    @allure.description("""
    Test details api module

    Expect correct response.
    """)
    def test_get_ip_details_by_url(self):
        url = "example.com"
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_ip_details_by_url(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_equal(resp.status_code, 200, "Check if correct status code was returned")
        json_data = json.loads(resp.data.decode('utf-8'))
        info(json_data)
        assert_type(json_data, dict, "Check if returned result is of correct type")
        assert_not_empty(json_data, "Check if returned dict is not empty")
        field = "details"
        assert_dict_contains_key(json_data, field, "Check if returned dict contains '{}' key".format(field))
        field = "country"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "ip"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "asn"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))

    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_ip_details_by_url_no_url(self):
        ip = token_hex(6)
        url_body = {
            "ip": ip
        }
        info("Requested url body: {}".format(url_body))
        with allure.step("[STEP] Check if proper exception is raised: {}".format(BadRequest)):
            with pytest.raises(BadRequest, match="'url' is a required property"):
                get_ip_details_by_url(url_body)

    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_ip_details_by_url_wrong_url(self):
        url = token_hex(32)
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_ip_details_by_url(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_equal(resp.status_code, 202, "Check if correct status code was returned")

    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_ip_details_by_url_wrong_url(self):
        url = token_hex(32)
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_ip_details_by_url(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_equal(resp.status_code, 202, "Check if correct status code was returned")