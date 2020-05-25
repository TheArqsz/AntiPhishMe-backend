import pytest
import allure

from hamcrest import * 
from config import logging as log
from json import loads, JSONDecodeError
from pycerthole import CertHole

def data_to_json(data):
    __tracebackhide__ = True
    try:
        log.info(type(loads(data.decode('utf-8'))))
        return loads(data.decode('utf-8'))
    except TypeError:
        pytest.fail("Passed data \"{}\" is not valid JSON".format(data.decode('utf-8')))

def info(message, pre=False, post=False, raw=False):
    if pre:
        m = "[PRE] {}".format(message)     
    elif post:
        m = "[POST] {}".format(message)
    elif raw:
        m = "{}".format(message)
    else:
        m = "[STEP] {}".format(message)

    with allure.step("{}".format(m)):
        log.info(m)

def error(message):
    log.error("[ERROR] {}".format(message))

def assert_equal(real, expected, message=None):
    __tracebackhide__ = True
    if message:
        with allure.step("[STEP] {}".format(message)):
            with allure.step("Assert real \"{}\" equal to expected \"{}\"".format(real, expected)):
                info("Real value is: {}".format(real), raw=True)
                info("Expected value is: {}".format(expected), raw=True)
                assert_that(real, equal_to(expected))
    else:
        with allure.step("Assert real \"{}\" equal to expected \"{}\"".format(real, expected)):
            info("Real value is: {}".format(real), raw=True)
            info("Expected value is: {}".format(expected), raw=True)
            assert_that(real, equal_to(expected))

def assert_dict_contains_key(d, key, message=None):
    __tracebackhide__ = True
    if message:
        with allure.step("[STEP] {}".format(message)):
            with allure.step("Assert {} contains {}".format(d, key)):
                info("Key is: {}".format(key), raw=True)
                info("Dictionary is: {}".format(d), raw=True)
                assert_that(d, has_key(key))
    else:
        with allure.step("Assert {} contains {}".format(d, key)):
            info("Key is: {}".format(key), raw=True)
            info("Dictionary is: {}".format(d), raw=True)
            assert_that(d, has_key(key))

def get_test_phishing_domain():
    __tracebackhide__ = True
    ch = CertHole()
    return ch.get_data('txt')[0].domain_address