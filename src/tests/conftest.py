import pytest

from datetime import datetime

def pytest_report_header(config):
    info = [
        "Tests run at: {}".format(datetime.now())
    ]
    return info