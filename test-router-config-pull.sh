#!/bin/bash

compare_configs() {
  C1=$1
  C2=$2

  # Remove 1st line
  tail -n +2 /tmp/${C1} > /tmp/${C1}.1d
  tail -n +2 /tmp/${C2} > /tmp/${C2}.1d

  CHANGES=$(diff ${C1}.1d ${C2}.1d)
  if [ $? != 0 ];then
    notify_slack_of_changes "${CHANGES}"
    push_new_config "${C1}"
  fi
  rm /tmp/${C1}.1d /tmp/${C2}.1d
}

notify_slack_of_changes() {
  CHANGES=$1
  TIMESTAMP=$(date "+%Y-%m-%dT%H:%M:%S.%6NZ")
  post_slack_msg "'${TIMESTAMP}' | Router config has been updated:\n\n'${CHANGES}'"
}

push_new_config() {
  NEW_CONFIG=$1

  cd ${REPO_DIR}
  cp /tmp/${NEW_CONFIG} .
  git add ${NEW_CONFIG}
  git commit -m "Changes made to mikrotik.conf"
  git push origin
  notify_slack_of_push
}

notify_slack_of_push() {
  TIMESTAMP=$(date "+%Y-%m-%dT%H:%M:%S.%6NZ")
  post_slack_msg "'${TIMESTAMP}' | Updated router config has been committed"
}

post_slack_msg() {
  MSG=$1
  curl \
    -H "Content-type: application/json" \
    --data '{
              "channel": "ansible-notifications",
              "blocks": [{
                "type": "section",
                "text": {
                  "type": "mrkdwn",
                  "text": "'${MSG}'"
                }
              }]
            }' \
    -X POST ${ANSBL_WEBHOOK} > /dev/null 2>&1
}

# Vars
SVC_ACCT=robackup
ROUTER=192.168.11.1
CURRENT_CONFIG=mikrotik.conf.current
REPO_DIR=~/projects/ans
PREVIOUS_CONFIG=mikrotik.conf

### MAIN ###

#if [ $(whoami) != '${SVC_ACCT}' ];then
#  echo ""
#  echo "This script must be run as ${SVC_ACCT} user"
#  exit 1
#fi
#
cd /tmp
ssh ${SVC_ACCT}@${ROUTER} /export > ${CURRENT_CONFIG}
compare_configs ${CURRENT_CONFIG} ${PREVIOUS_CONFIG}

