#!/usr/bin/env bash

if [ $TRAVIS_BRANCH != $GIT_BRANCH_DEV ]; then
    echo "Current branch doesn't match requirements for docker image building"
    exit 0
fi

echo "Checking if image $LOCAL_DOCKER_IMAGE is operational"
is_present=`docker ps | grep -c $LOCAL_DOCKER_IMAGE`

if [ $is_present -eq 1 ]
then
    echo "Image \"$LOCAL_DOCKER_IMAGE\" exists - checking stability"
else
    echo "Image \"$LOCAL_DOCKER_IMAGE\" is not working - exiting"
    export LOCAL_DOCKER_IMAGE_STATUS="not working"
    exit 1
fi

response=$(curl --write-out %{http_code} --silent --output /dev/null $LOCAL_DOCKER_SERVER)
if [ $response -eq 404 ]
then
    echo "Image \"$LOCAL_DOCKER_IMAGE\" is working"
    export LOCAL_DOCKER_IMAGE_STATUS="working"
    exit 0
else    
    echo "Image \"$LOCAL_DOCKER_IMAGE\" is not working"
    export LOCAL_DOCKER_IMAGE_STATUS="not working"
    exit 1
fi