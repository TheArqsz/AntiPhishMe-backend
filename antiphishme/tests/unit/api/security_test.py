import allure
from unittest import mock
import pytest

from antiphishme.tests.test_helpers import (
    assert_dict_contains_key,
    assert_not_empty,
    assert_equal,
    assert_type,
    assert_exception,
    info
)

from antiphishme.src.api import security
from secrets import token_hex

from antiphishme.src.config import AUTH_API_KEY
from werkzeug.exceptions import Unauthorized

@allure.epic("api")
@allure.parent_suite("Unit tests")
@allure.story('Unit')
@allure.suite("api")
@allure.sub_suite("security")
class Tests:

    @allure.description("""
    Test security api module

    Expect authorized.
    """)
    def test_verify_api(self):
        info("Requested api key: {}".format(AUTH_API_KEY))
        result = security.verify_api(apikey=AUTH_API_KEY, required_scopes=None)
        assert_type(result, dict, "Check if returned result is of correct type")
        assert_not_empty(result, "Check if returned dict is not empty")
        field = "auth_type"
        expected = "apiKey"
        assert_dict_contains_key(result, field, "Check if returned dict contains '{}' key".format(field))
        assert_equal(result[field], expected, "Check if correct auth type was returned")
        field = "apiKey"
        expected = AUTH_API_KEY
        assert_dict_contains_key(result, field, "Check if returned dict contains '{}' key".format(field))
        assert_equal(result[field], expected, "Check if correct api key was returned")

    @allure.description("""
    Test security api module

    Expect unauthorized.
    """)
    def test_verify_api_unauthorized(self):
        api_key = token_hex(6)
        info("Requested api key: {}".format(api_key))
        with allure.step("[STEP] Check if proper exception is raised: {}".format(Unauthorized)):
            with pytest.raises(Unauthorized):
                security.verify_api(apikey=api_key, required_scopes=None)