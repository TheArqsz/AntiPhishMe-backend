#!/usr/bin/env sh

if [ $TRAVIS_BRANCH != $GIT_BRANCH_DEV ]; then
    echo "Current branch doesn't match requirements for pushing images"
    exit 0
fi

if [ -z "${DOCKER_SLACK_URL}" ]
then
    echo "DOCKER_SLACK_URL env var cannot be found - exiting"
    exit 0
fi

if [ -z "${DOCKER_TOKEN}" ]
then
    echo "DOCKER_TOKEN env var cannot be found - exiting"
    exit 0
fi

if [ -z "${DOCKER_USERNAME}" ]
then
    echo "DOCKER_USERNAME env var cannot be found - exiting"
    exit 0
fi

if [ -z "${REMOTE_DOCKER_IMAGE}" ]
then
    echo "REMOTE_DOCKER_IMAGE env var cannot be found - exiting"
    exit 0
fi

echo "Logging in to DockerHub"
echo "$DOCKER_TOKEN" | docker login --username "$DOCKER_USERNAME" --password-stdin

echo "Tagging image $LOCAL_DOCKER_IMAGE"
docker tag $LOCAL_DOCKER_IMAGE:latest $DOCKER_USERNAME/$REMOTE_DOCKER_IMAGE:latest

echo "Pushing image $DOCKER_USERNAME/$REMOTE_DOCKER_IMAGE:latest"
docker push $DOCKER_USERNAME/$REMOTE_DOCKER_IMAGE:latest

echo "Sending notification"
curl -X POST \
    --data-urlencode "payload={\
    \"blocks\": [ \
		{ \
			\"type\": \"section\", \
			\"text\": { \
				\"type\": \"mrkdwn\", \
				\"text\": \"Docker image *$LOCAL_DOCKER_IMAGE* status: \`working\`\" \
			} \
		}, \
		{ \
			\"type\": \"section\", \
			\"text\": { \
				\"type\": \"mrkdwn\", \
				\"text\": \"Image can be found here: <https://hub.docker.com/r/$DOCKER_USERNAME/$REMOTE_DOCKER_IMAGE|$DOCKER_USERNAME/$REMOTE_DOCKER_IMAGE>\" \
			} \
		} \
	] \
        }" \
        ${DOCKER_SLACK_URL}