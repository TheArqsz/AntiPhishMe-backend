import allure

from antiphishme.src.api_modules.crtsh import get_results
from antiphishme.tests.test_helpers import (
    assert_true,
    assert_none,
    assert_not_empty,
    assert_type,
    info
)

@allure.epic("api_modules")
@allure.parent_suite("Unit tests")
@allure.suite("api_modules")
@allure.sub_suite("crt.sh")
class Tests:

    @allure.description("""
    Test crt.sh api module

    Expect more than one record.
    """)
    def test_get_cert_results(self):
        domain = "example.com"
        info("Requested domain - {}".format(domain))
        l = get_results(domain)
        assert_type(l, dict, "Check if returned object with certificate details is proper dict")
        assert_not_empty(l, "Check if cert details dict is not empty")

    @allure.description("""
    Test crt.sh api module

    Expect empty result.
    """)
    def test_get_cert_results_empty(self):
        domain = "http://."
        info("Requested domain - {}".format(domain))
        l = get_results(domain)
        assert_none(l, "Check if returned object with unexisting certificate details is empty/None")