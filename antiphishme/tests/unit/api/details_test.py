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
    assert_is_in,
    info
)

from antiphishme.src.api.details import (
    get_ip_details,
    get_ip_details_by_url,
    get_whois_details,
    get_sfbrowsing_details,
    get_crtsh_details,
    get_urlscan_details,
    get_entropy_details
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

    Expect 202.
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

    Expect correct response.
    """)
    def test_get_whois_details(self):
        url = "example.com"
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_whois_details(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_equal(resp.status_code, 200, "Check if correct status code was returned")
        json_data = json.loads(resp.data.decode('utf-8'))
        assert_type(json_data, dict, "Check if returned result is of correct type")
        assert_not_empty(json_data, "Check if returned dict is not empty")
        field = "details"
        assert_dict_contains_key(json_data, field, "Check if returned dict contains '{}' key".format(field))
        field = "registrar"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "org"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "creation_date"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "name"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))

    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_get_whois_details_no_url(self):
        ip = token_hex(6)
        url_body = {
            "ip": ip
        }
        info("Requested url body: {}".format(url_body))
        with allure.step("[STEP] Check if proper exception is raised: {}".format(BadRequest)):
            with pytest.raises(BadRequest, match="'url' is a required property"):
                get_whois_details(url_body)

    @allure.description("""
    Test details api module

    Expect 202.
    """)
    def test_get_whois_details_wrong_url(self):
        url = token_hex(32)
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_whois_details(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_equal(resp.status_code, 202, "Check if correct status code was returned")
    
    @allure.description("""
    Test details api module

    Expect correct response.
    """)
    def test_get_sfbrowsing_details(self):
        url = "example.com"
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_sfbrowsing_details(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_equal(resp.status_code, 200, "Check if correct status code was returned")
        json_data = json.loads(resp.data.decode('utf-8'))
        assert_type(json_data, dict, "Check if returned result is of correct type")
        assert_not_empty(json_data, "Check if returned dict is not empty")
        field = "details"
        assert_dict_contains_key(json_data, field, "Check if returned dict contains '{}' key".format(field))
        field = "url"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        assert_equal(json_data['details'][field], url, "Check if correct url was returned")
        field = "malicious"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        
    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_get_sfbrowsing_details_no_url(self):
        ip = token_hex(6)
        url_body = {
            "ip": ip
        }
        info("Requested url body: {}".format(url_body))
        with allure.step("[STEP] Check if proper exception is raised: {}".format(BadRequest)):
            with pytest.raises(BadRequest, match="'url' is a required property"):
                get_sfbrowsing_details(url_body)

    @allure.description("""
    Test details api module

    Expect correct response.
    """)
    def test_get_crtsh_details(self):
        url = "example.com"
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_crtsh_details(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_is_in(resp.status_code, [200, 202], "Check if correct status code was returned")
        if resp.status_code == 202:
            info("Returned 202 - skipping rest of asserts")
            return
        json_data = json.loads(resp.data.decode('utf-8'))
        assert_type(json_data, dict, "Check if returned result is of correct type")
        assert_not_empty(json_data, "Check if returned dict is not empty")
        field = "details"
        assert_dict_contains_key(json_data, field, "Check if returned dict contains '{}' key".format(field))
        field = "caid"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "registered_at"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "subject"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "issuer"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "multi_dns_amount"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "org_name"
        assert_dict_contains_key(json_data['details']['subject'], field, "Check if returned dict contains '{}' key".format(field))
        field = "country"
        assert_dict_contains_key(json_data['details']['subject'], field, "Check if returned dict contains '{}' key".format(field))
        field = "common_name"
        assert_dict_contains_key(json_data['details']['issuer'], field, "Check if returned dict contains '{}' key".format(field))
        
    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_get_crtsh_details_no_url(self):
        ip = token_hex(6)
        url_body = {
            "ip": ip
        }
        info("Requested url body: {}".format(url_body))
        with allure.step("[STEP] Check if proper exception is raised: {}".format(BadRequest)):
            with pytest.raises(BadRequest, match="'url' is a required property"):
                get_crtsh_details(url_body)

    @allure.description("""
    Test details api module

    Expect 202.
    """)
    def test_get_crtsh_details_wrong_url(self):
        url = token_hex(32)
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_crtsh_details(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_equal(resp.status_code, 202, "Check if correct status code was returned")

    @allure.description("""
    Test details api module

    Expect correct response.
    """)
    def test_get_urlscan_details(self):
        url = "example.com"
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_crtsh_details(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_is_in(resp.status_code, [200, 202], "Check if correct status code was returned")
        if resp.status_code == 202:
            info("Returned 202 - skipping rest of asserts")
            return
        json_data = json.loads(resp.data.decode('utf-8'))
        assert_type(json_data, dict, "Check if returned result is of correct type")
        assert_not_empty(json_data, "Check if returned dict is not empty")
        field = "details"
        assert_dict_contains_key(json_data, field, "Check if returned dict contains '{}' key".format(field))
        field = "caid"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "registered_at"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "subject"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "issuer"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "multi_dns_amount"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        field = "org_name"
        assert_dict_contains_key(json_data['details']['subject'], field, "Check if returned dict contains '{}' key".format(field))
        field = "country"
        assert_dict_contains_key(json_data['details']['subject'], field, "Check if returned dict contains '{}' key".format(field))
        field = "common_name"
        assert_dict_contains_key(json_data['details']['issuer'], field, "Check if returned dict contains '{}' key".format(field))
        
    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_get_urlscan_details_no_url(self):
        ip = token_hex(6)
        url_body = {
            "ip": ip
        }
        info("Requested url body: {}".format(url_body))
        with allure.step("[STEP] Check if proper exception is raised: {}".format(BadRequest)):
            with pytest.raises(BadRequest, match="'url' is a required property"):
                get_crtsh_details(url_body)

    @allure.description("""
    Test details api module

    Expect 202.
    """)
    def test_get_urlscan_details_wrong_url(self):
        url = token_hex(32)
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_crtsh_details(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_equal(resp.status_code, 202, "Check if correct status code was returned")

    @allure.description("""
    Test details api module

    Expect correct response.
    """)
    def test_get_entropy_details(self):
        url = "exampleawdawdefgrgdheqafrty3452rf.comc"
        url_body = {
            "url": url
        }
        info("Requested url body: {}".format(url_body))
        resp = get_entropy_details(url_body)
        assert_type(resp, Response, "Check if returned result is of correct type")
        assert_equal(resp.status_code, 200, "Check if correct status code was returned")
        json_data = json.loads(resp.data.decode('utf-8'))
        assert_type(json_data, dict, "Check if returned result is of correct type")
        assert_not_empty(json_data, "Check if returned dict is not empty")
        field = "details"
        assert_dict_contains_key(json_data, field, "Check if returned dict contains '{}' key".format(field))
        field = "entropy"
        assert_dict_contains_key(json_data['details'], field, "Check if returned dict contains '{}' key".format(field))
        assert_equal(json_data['details'][field], pytest.approx(json_data['details'][field], 0.01), "Check if returned entropy is properly rounded to 2 decimal places")
    
    @allure.description("""
    Test details api module

    Expect BadRequest.
    """)
    def test_get_entropy_details_no_url(self):
        ip = token_hex(6)
        url_body = {
            "ip": ip
        }
        info("Requested url body: {}".format(url_body))
        with allure.step("[STEP] Check if proper exception is raised: {}".format(BadRequest)):
            with pytest.raises(BadRequest, match="'url' is a required property"):
                get_entropy_details(url_body)


    # TODO somehow mock db and test levenstein and keywords