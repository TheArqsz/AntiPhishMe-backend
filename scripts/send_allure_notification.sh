#!/usr/bin/env sh

if [ $TRAVIS_BRANCH != $GIT_BRANCH_DEV ]; then
    echo "Current branch doesn't match requirements to send notification"
    exit 0
fi

if [ -z "${ALLURE_HOST}" ]
then
    echo "ALLURE_HOST env var cannot be found - exiting"
    exit 0
fi

if [ -z "${SLACK_URL}" ]
then
    echo "SLACK_URL env var cannot be found - exiting"
    exit 0
fi

curl -X POST \
    --data-urlencode "payload={\
        \"text\": \"Allure report sent successfully.
It can be found <${ALLURE_HOST}|here>\"
        }" \
        ${SLACK_URL}