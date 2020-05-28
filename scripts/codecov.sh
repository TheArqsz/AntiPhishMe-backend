#!/usr/bin/env bash

if [ $TRAVIS_BRANCH != $GIT_BRANCH_DEV ]; then
    echo "Current branch doesn't match requirements to check code coverage"
    exit 0
fi

codecov