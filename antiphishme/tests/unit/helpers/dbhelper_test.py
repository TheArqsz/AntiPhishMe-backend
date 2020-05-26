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


from antiphishme.src.models import (
    goodies_model,
    baddies_model,
    ip_model,
    certs_model
)

from antiphishme.src.helpers import db_helper
from antiphishme.src.api_modules import ip_module
from secrets import token_hex

@allure.epic("helpers")
@allure.parent_suite("Unit tests")
@allure.suite("helpers")
@allure.sub_suite("dbhelper")
class Tests:

    @allure.description("""
    Test db_helper helpers module
    Test add_cert method

    Expect correct cert id.
    """)
    @mock.patch.object(certs_model.Certs, 'add_cert')
    def test_add_cert_correct(self, mock_add_cert):

        # Mock Cert response
        mocked_id = 1
        mock_add_cert.return_value = mocked_id
        info("Created mock Cert with id: {}".format(mocked_id))

        status, cid = db_helper.add_cert("test.com")
        assert_true(status, "Check if method return correct status")
        assert_equal(cid, mocked_id, "Check if method returned correct id")

    @allure.description("""
    Test db_helper helpers module
    Test add_cert method

    Expect -1 as cert id.
    """)
    @mock.patch.object(certs_model.Certs, 'add_cert')
    def test_add_cert_invalid(self, mock_add_cert):

        # Mock Cert response
        mocked_id = -1
        mock_add_cert.return_value = mocked_id
        info("Created mock Cert with id: {}".format(mocked_id))

        status, cid = db_helper.add_cert(".")
        assert_false(status, "Check if method return correct status")
        assert_equal(cid, mocked_id, "Check if method returned correct id")
    
    @allure.description("""
    Test db_helper helpers module
    Test add_ip method

    Expect correct ip id.
    """)    
    def test_add_ip_correct(self): #, mock_get_ip_details):
        ip = "127.0.0.1"

        status, cid = db_helper.add_ip(ip)
        assert_true(status, "Check if method return correct status")
        assert_type(cid, int, "Check if id is correct int")

    @allure.description("""
    Test db_helper helpers module
    Test add_baddie method

    Expect correct baddie id.
    """)    
    @mock.patch.object(baddies_model.Baddies, 'add_baddie')
    def test_add_baddie_correct(self, mock_add_baddie):
        mocked_id = 1
        mock_add_baddie.return_value = mocked_id
        info("Created mock Baddie with id: {}".format(mocked_id))

        cid = db_helper.add_baddie(None, None, None, None, None, None, None)
        assert_type(cid, int, "Check if id is correct int")
        assert_equal(cid, mocked_id, "Check if method returned correct id")

# TODO More unit tests