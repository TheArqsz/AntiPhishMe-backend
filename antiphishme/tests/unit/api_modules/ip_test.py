import allure

from antiphishme.src.api_modules.ip_module import get_ip, get_ip_details
from antiphishme.tests.test_helpers import (
    assert_true,
    assert_equal,
    assert_none,
    assert_type,
    assert_not_empty,
    info
)

@allure.epic("api_modules")
@allure.parent_suite("Unit tests")
@allure.story('Unit')
@allure.suite("api_modules")
@allure.sub_suite("ip")
class Tests:

    @allure.description("""
    Test ip api module

    Expect proper ip for given domain.
    """)
    def test_get_ip(self):
        domain = "google.com"
        info("Requested domain - {}".format(domain))
        ip = get_ip(domain)
        info("Returned ip: {}".format(ip))
        assert_true(ip.count('.') == 3, "Check if returned ip is correct ip")

    @allure.description("""
    Test ip api module

    Send unexisting domain and expect None.
    """)
    def test_get_ip_unexisting(self):
        domain = "."
        info("Requested domain - {}".format(domain))
        ip = get_ip(domain)
        info("Returned ip: {}".format(ip))
        assert_none(ip, "Check if result for get_ip is None")

    @allure.description("""
    Test ip api module

    Send correct ip and expect details dict.
    """)
    def test_get_ip_details(self):
        ip = "8.8.8.8"
        info("Requested ip - {}".format(ip))
        details = get_ip_details(ip)
        assert_type(details, dict, "Check if returned results are of type dict")
        assert_not_empty(details, "Check if returned results are not empty")

    @allure.description("""
    Test ip api module

    Send reserved ip and expect proper response.
    """)
    def test_get_ip_details_reserved_range(self):
        ip = "127.0.0.1"
        info("Requested ip - {}".format(ip))
        details = get_ip_details(ip)
        assert_type(details, dict, "Check if returned results are of type dict")
        assert_not_empty(details, "Check if returned results are not empty")
        field = 'status'
        expected = 'reserved_range'
        assert_equal(details[field], expected, "Check if returned status is equal to expected one")
        field = 'ip'
        expected = ip
        assert_equal(details[field], expected, "Check if returned ip is equal to expected one")

    @allure.description("""
    Test ip api module

    Send wrong ip and expect None.
    """)
    def test_get_ip_details_wrong_ip(self):
        ip = "abc"
        info("Requested ip - {}".format(ip))
        details = get_ip_details(ip)
        assert_none(details, "Check if returned results are empty/None")