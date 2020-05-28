#!/usr/bin/env sh

if [ $TRAVIS_BRANCH != $GIT_BRANCH_DEV ]; then
    echo "Current branch doesn't match requirements to be published as report"
    exit 0
fi

echo "Creating ssh key"
mkdir -p ~/.ssh \
&& ssh_key=`echo "${SSH_ALLURE_KEY}" | base64 -d` \
&& echo "${ssh_key}" | sed -r 's/_/\n/g' > ~/.ssh/allure_id_rsa \
&& chmod og-rwx ~/.ssh/allure_id_rsa

echo "Clear remote"
ssh -i ~/.ssh/allure_id_rsa -oStrictHostKeyChecking=no -oBatchMode=yes allure@${SSH_ALLURE_HOST} \
"rm -rf ${SSH_ALLURE_REMOTE_PATH}/*.json ${SSH_ALLURE_REMOTE_PATH}/*.txt"

echo "Uploading files"
rsync -Pav -e 'ssh -i ~/.ssh/allure_id_rsa -oStrictHostKeyChecking=no -oBatchMode=yes' \
    ${PWD}/antiphishme/tests/results/* "allure@${SSH_ALLURE_HOST}:${SSH_ALLURE_REMOTE_PATH}/" 

echo "Cleaning ssh key"
rm -f ~/.ssh/allure_id_rsa