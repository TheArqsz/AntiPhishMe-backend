import pytest
import os
import sys
import json
from datetime import datetime
from subprocess import check_output
import logging as log

def pytest_report_header(config):
    # Create allure envs
    allure_generate_environment(config)
    #Modify header
    info = [
        "Tests run at: {}".format(datetime.now()),
        "Allure results: {}".format(config.option.allure_report_dir)
    ]
    return info

def allure_generate_environment(config):
    if config.option.allure_report_dir is None:
        return
    else:
        allure_dir = config.option.allure_report_dir

    envs = {
        "URLSCAN-API-KEY": "not set" if not os.getenv('URLSCAN_API_KEY') else "set",
        "SAFEBROWSING-API-KEY": "not set" if not os.getenv('SAFEBROWSING_API_KEY') else "set",
        "ENVIRONMENT": "{}: {}".format(os.uname()[1], os.uname()[0]) \
            if not os.getenv('TRAVIS_OS_NAME') else "TRAVIS CI: {}".format(os.getenv("TRAVIS_OS_NAME")),
        "PYTHON-VERSION": "{}".format(sys.version.split('\n')[0]) \
            if not os.getenv('TRAVIS_PYTHON_VERSION') else "{}".format(os.getenv("TRAVIS_PYTHON_VERSION")),
        "TEST-BRANCH": "{}".format(check_output("git rev-parse --abbrev-ref HEAD".split(' ')).decode('utf-8').strip()) \
            if not os.getenv('TRAVIS_BRANCH') else "{}".format(os.getenv("TRAVIS_BRANCH")),
    }
    with open(os.path.join(allure_dir, 'environment.properties'), 'w') as w:
        for key in envs.keys():
            w.write("{}={}\n".format(key, envs[key]))
    
    with open(os.path.join(allure_dir, 'executor.json'), 'w') as w:
        data = {
            "name": "local" if not os.getenv("TRAVIS_JOB_WEB_URL") else 'TRAVIS CI',
            "type": "local" if not os.getenv("TRAVIS_JOB_WEB_URL") else 'travis',
            "url": "localhost" if not os.getenv("TRAVIS_JOB_WEB_URL") else "http://travis-ci.com",
            "buildOrder": 1 if not os.getenv("TRAVIS_BUILD_NUMBER") else os.getenv('TRAVIS_BUILD_NUMBER'),
            "buildName": "local#1" if not os.getenv("TRAVIS_BUILD_NUMBER") \
                else "{}#{}".format('travis',os.getenv("TRAVIS_BUILD_NUMBER")),
            "buildUrl": "http://localhost:4040" if not os.getenv("TRAVIS_BUILD_WEB_URL") else os.getenv("TRAVIS_BUILD_WEB_URL"),
            "reportUrl": "http://localhost:4040" if not os.getenv("ALLURE_HOST") else os.getenv("ALLURE_HOST"),
            "reportName": "AntiPhishMe allure report"
        }
        json.dump(data, w)

