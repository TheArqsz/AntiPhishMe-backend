import allure

from antiphishme.src.api_modules.entropy import get_entropy
from antiphishme.tests.test_helpers import (
    assert_true,
    assert_equal,
    info
)

@allure.epic("api_modules")
@allure.parent_suite("Unit tests")
@allure.story('Unit')
@allure.suite("api_modules")
@allure.sub_suite("entropy")
class Tests:

    @allure.description("""
    Test entropy api module

    Expect entropy equal 0.
    """)
    def test_get_entropy_zero(self):
        string = "aaa"
        info("Checked string - {}".format(string))
        e = get_entropy(string)
        info("Calculated entropy: {}".format(e))
        assert_equal(e, 0, "Check if calculated entropy is equal to predicted one")

    @allure.description("""
    Test entropy api module

    Expect entropy bigger than 0.
    """)
    def test_get_entropy(self):
        string = "ab"
        info("Checked string - {}".format(string))
        e = get_entropy(string)
        info("Calculated entropy: {}".format(e))
        assert_true(e > 0,"Check if calculated entropy is bigger than 0")
        assert_equal(e, 1, "Check if calculated entropy is equal to predicted one")