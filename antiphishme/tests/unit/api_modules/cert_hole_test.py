import allure
from antiphishme.src.api_modules.cert_hole import get_phishing_domains
from antiphishme.tests.test_helpers import (
    assert_type,
    assert_not_empty
)

@allure.epic("api_modules")
@allure.parent_suite("Unit tests")
@allure.suite("api_modules")
@allure.sub_suite("certhole")
@allure.description("""
Test certhole api module

Expect more than one record.
""")
def test_get_phishing_domains():
    l = get_phishing_domains()
    assert_type(l, list, "Check if returned object with phishing domains is proper list")
    assert_not_empty(l, "Check if list of phishing domains is not empty")