import allure
from unittest import mock
import pytest

from antiphishme.tests.test_helpers import (
    assert_equal,
    assert_type,
    info
)

from antiphishme.src.phishing import url_verifier as uv

from antiphishme.src.models import (
    goodies_model,
    baddies_model,
    ip_model,
    certs_model
)

@allure.epic("phishing")
@allure.parent_suite("Unit tests")
@allure.story('Unit')
@allure.suite("phishing")
@allure.sub_suite("urlverifier")
class Tests:

    @allure.description("""
    Test url_verifier phishing module

    Test verify_domain_in_baddies
    Expect malicious.
    """)
    @mock.patch.object(baddies_model.Baddies, 'get_all_baddies')
    def test_verify_domain_in_baddies_exists(self, mock_get_all_baddies):

        # Mock Baddies response
        mocked_list = [
            {
                "domain_name": "not-example.com"
            },
            {
                "domain_name": "example.com"
            }
        ]
        mock_get_all_baddies.return_value = mocked_list
        info("Created mock Baddies list: {}".format(mocked_list))

        test_domain = "example.com"
        info("Requested domain: {}".format(test_domain))
        result = uv.verify_domain_in_baddies(test_domain)
        assert_type(result, bool, "Check if returned result is of correct type")
        assert_equal(result, True, "Check if method returned correct verdict")

    @allure.description("""
    Test url_verifier phishing module

    Test verify_domain_in_baddies
    Expect good.
    """)
    @mock.patch.object(baddies_model.Baddies, 'get_all_baddies')
    def test_verify_domain_in_baddies_not_exists(self, mock_get_all_baddies):

        # Mock Baddies response
        mocked_list = [
            {
                "domain_name": "example.com"
            },
            {
                "domain_name": "not-example.com"
            }
        ]
        mock_get_all_baddies.return_value = mocked_list
        info("Created mock Baddies list: {}".format(mocked_list))

        test_domain = "definitely-not-example.com"
        info("Requested domain: {}".format(test_domain))
        result = uv.verify_domain_in_baddies(test_domain)
        assert_type(result, bool, "Check if returned result is of correct type")
        assert_equal(result, False, "Check if method returned correct verdict")