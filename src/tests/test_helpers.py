import pytest
import allure
import random
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

def assert_true(expresion, message=None):
    __tracebackhide__ = True
    if message:
        with allure.step("[STEP] {}".format(message)):
            with allure.step("Assert that \"{}\" is true".format(expresion)):
                assert_that(expresion, is_not(False))
    else:
        with allure.step("Assert that \"{}\" is true".format(expresion)):
            assert_that(expresion, is_not(False))

def assert_false(expresion, message=None):
    __tracebackhide__ = True
    if message:
        with allure.step("[STEP] {}".format(message)):
            with allure.step("Assert that \"{}\" is false".format(expresion)):
                assert_that(expresion, is_(False))
    else:
        with allure.step("Assert that \"{}\" is false".format(expresion)):
            assert_that(expresion, is_(False))

def assert_none(variable, message=None):
    __tracebackhide__ = True
    if message:
        with allure.step("[STEP] {}".format(message)):
            with allure.step("Assert that \"{}\" is None".format(variable)):
                assert_that(variable, none())
    else:
        with allure.step("Assert that \"{}\" is None".format(variable)):
            assert_that(variable, none())

def assert_exception(expression, exc, message=None, args=None):
    __tracebackhide__ = True
    if message:
        with allure.step("[STEP] {}".format(message)):
            with allure.step("Assert that \"{}\" is thrown".format(exc)):
                if args:
                    assert_that(calling(expression, args), raises(exc))
                else:
                    assert_that(calling(expression), raises(exc))
    else:
        with allure.step("Assert that \"{}\" is thrown".format(exc)):
            if args:
                assert_that(calling(expression, args), raises(exc))
            else:
                assert_that(calling(expression), raises(exc))
    
def assert_no_exception(expression, exc, message=None):
    __tracebackhide__ = True
    if message:
        with allure.step("[STEP] {}".format(message)):
            with allure.step("Assert that \"{}\" is not thrown".format(exc)):
                assert_that(calling(expression), not_(raises(exc)))
    else:
        with allure.step("Assert that \"{}\" is not thrown".format(exc)):
            assert_that(calling(expression), not_(raises(exc)))

def assert_not_empty(collection, message=None):
    __tracebackhide__ = True
    if message:
        with allure.step("[STEP] {}".format(message)):
            with allure.step("Assert that collection \"{}\" is not empty".format(collection.__class__)):
                log.info("Collection: {}".format(collection))
                assert_that(collection, is_(not_(empty())))
    else:
        with allure.step("Assert that collection \"{}\" is not empty".format(collection.__class__)):
            log.info("Collection: {}".format(collection))
            assert_that(collection, is_(not_(empty())))

def assert_type(o, t, message=None):
    __tracebackhide__ = True
    if message:
        with allure.step("[STEP] {}".format(message)):
            with allure.step("Assert that object \"{}\" is of type {}".format(o.__class__, t)):
                log.info("Object: {}".format(o))
                assert_that(o, instance_of(t))
    else:
        with allure.step("Assert that object \"{}\" is of type {}".format(o.__class__, t)):
            log.info("Object: {}".format(o))
            assert_that(o, instance_of(t))

def get_test_phishing_domain():
    __tracebackhide__ = True
    ch = CertHole()
    l = ch.get_data('txt')
    return (random.choice(l)).domain_address