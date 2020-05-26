import allure
from unittest import mock
import pytest

from antiphishme.tests.test_helpers import (
    assert_true,
    assert_equal,
    assert_none,
    assert_type,
    assert_false,
    info
)

from antiphishme.src.api_modules.keywords import match_keyword
from antiphishme.src.models.goodies_model import Goodies
from faker import Faker

@allure.epic("api_modules")
@allure.parent_suite("Unit tests")
@allure.suite("api_modules")
@allure.sub_suite("keywords")
class Tests:

    @allure.description("""
    Test keywords api module

    Expect match for given keyword.
    """)
    @mock.patch.object(Goodies, 'get_all_goodies')
    def test_match_keyword(self, mock_goodie):

        fake = Faker()
        mocked_keyword = fake.domain_word()
        # Mock Goodies response
        mock_goodie.return_value = [{
            'good_keyword': mocked_keyword
        }]
        info("Created mock Goodie with keyword: {}".format(mocked_keyword))

        domain = "{}x.com".format(mocked_keyword)
        info("Requested domain - {}".format(domain))
        l = match_keyword(domain)
        assert_type(l, tuple, "Check if proper tuple is returned")
        assert_true(l[0], "Check if keyword matches domain")
        assert_equal(l[1], mocked_keyword, "Check if returned keyword is equal to mocked one")

    @allure.description("""
    Test keywords api module

    Expect not match for given keyword.
    """)
    @mock.patch.object(Goodies, 'get_all_goodies')
    def test_not_match_keyword(self, mock_goodie):

        fake = Faker()
        mocked_keyword = fake.domain_word()
        # Mock Goodies response
        mock_goodie.return_value = [{
            'good_keyword': mocked_keyword
        }]
        info("Created mock Goodie with keyword: {}".format(mocked_keyword))
        while 1:
            mocked_domain = fake.domain_name()
            if mocked_keyword in mocked_domain:
                continue
            else:
                break
        info("Requested domain - {}".format(mocked_domain))
        l = match_keyword(mocked_domain)
        assert_type(l, tuple, "Check if proper tuple is returned")
        assert_false(l[0], "Check if keyword does not match domain")
        assert_none(l[1],  "Check if returned keyword is equal to None")
