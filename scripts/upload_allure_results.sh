#!/usr/bin/env sh

echo "Creating ssh key"
mkdir -p ~/.ssh \
&& ssh_key=`echo "${SSH_ALLURE_KEY}" | base64 -d` \
&& echo -e "${ssh_key}" | sed -r 's/_/\n/g' > ~/.ssh/allure_id_rsa \
&& chmod og-rwx ~/.ssh/allure_id_rsa

echo "Uploading files"
rsync -Pav -e 'ssh -i ~/.ssh/allure_id_rsa -oStrictHostKeyChecking=no' ../antiphishme/tests/results/* "allure@${SSH_ALLURE_HOST}:${SSH_ALLURE_REMOTE_PATH}/"

echo "Cleaning ssh key"
rm -f ~/.ssh/allure_id_rsa