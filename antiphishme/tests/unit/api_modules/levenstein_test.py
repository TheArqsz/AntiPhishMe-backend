import allure
import pytest

from antiphishme.tests.test_helpers import (
    assert_true,
    assert_equal,
    assert_none,
    assert_type,
    assert_false,
    info
)

from antiphishme.src.api_modules.levenstein import calculate_levenstein, levenstein_check
from faker import Faker

@allure.epic("api_modules")
@allure.parent_suite("Unit tests")
@allure.suite("api_modules")
@allure.sub_suite("levenstein")
class Tests:

    @allure.description("""
    Test levenstein api module

    Expect match for given keywords list.
    """)
    def test_levenstein_check(self):

        fake = Faker()
        keywords = [ fake.domain_word() for i in range(0,2)]
        info("Generated keyword: {}".format(keywords))

        proper_keyword = keywords[0]
        domain = "{}x.{}.{}awdawdawdfawytdawdrawd.com".format(proper_keyword, proper_keyword, proper_keyword)
        info("Requested domain - {}".format(domain))
        l = levenstein_check(keywords, domain.split('.'))
        assert_type(l, tuple, "Check if proper tuple is returned")
        assert_true(l[0], "Check if keyword matches domain")
        assert_equal(l[1], 1, "Check if keyword matches domain only one time")
        assert_equal(l[2], proper_keyword, "Check if proper keyword is returned")
        assert_equal(l[3], 1, "Check if proper levenstein distance is returned")

    @allure.description("""
    Test levenstein api module

    Expect no match for given keywords list.
    """)
    def test_levenstein_check_no_match(self):

        fake = Faker()
        keywords = [ fake.domain_word() ]
        info("Generated keyword: {}".format(keywords))

        domain = "{}x.com".format(fake.domain_word())
        info("Requested domain - {}".format(domain))
        l = levenstein_check(keywords, domain.split('.'))
        assert_type(l, tuple, "Check if proper tuple is returned")
        assert_false(l[0], "Check if keyword matches domain")
        assert_none(l[1], "Check if no keyword matches domain")
        assert_none(l[2], "Check if no keyword is returned")
        assert_none(l[3], "Check if no levenstein distance is returned")

    @allure.description("""
    Test levenstein api module

    Expect correct lev distance.
    """)
    def test_calculate_distance(self):

        base = "test"
        target = "tent"
        info("Base keyword: {}".format(base))
        info("Target keyword: {}".format(target))

        l = calculate_levenstein(base, target)
        assert_type(l, int, "Check if proper type is returned")
        assert_equal(l, 1, "Check if proper distance is calculated")
    
    @allure.description("""
    Test levenstein api module

    Expect zero lev distance.
    """)
    def test_calculate_distance_zero(self):

        base = "test"
        target = base
        info("Base keyword: {}".format(base))
        info("Target keyword: {}".format(target))

        l = calculate_levenstein(base, target)
        assert_type(l, int, "Check if proper type is returned")
        assert_equal(l, 0, "Check if proper distance is calculated")

   