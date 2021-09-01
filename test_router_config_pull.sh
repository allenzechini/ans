#!/bin/bash

usage() {
  echo "${0##*/}"
  echo ""
  echo "  Creates a copy of router config"
  echo "  If changes made, commits changes to git repo"
  echo ""
}

compare_configs() {
  C1=$1
  C2=$2

  diff ${C1} ${C2}
  if [ $? != 0 ];then
    notify_slack
    push_new_config ${C1}
  fi
}

notify_slack_of_change() {
  TIMESTAMP=$(date "+%Y-%m-%dT%H:%M:%S.%6NZ")
  curl \
    -H "Content-type: application/json" \
    --data '{
              "channel": "ansible-notifications",
              "blocks": [ {
                  "type": "section",
                  "text": {
                      "type": "mrkdwn",
                      "text": "'${TIMESTAMP}' | Router config has been updated"
                  }
              }]
            }' \
    -X POST ${ANSBL_WEBHOOK} > /dev/null 2>&1
}

push_new_config() {
  NEW_CONFIG=$1

  cd ${REPO_DIR}
  git add ${NEW_CONFIG}
  git commit -m "Changes made to mikrotik.conf"
  git push origin
  notify_slack_of_push
}

notify_slack_of_push() {
  TIMESTAMP=$(date "+%Y-%m-%dT%H:%M:%S.%6NZ")
  curl \
    -H "Content-type: application/json" \
    --data '{
              "channel": "ansible-notifications",
              "blocks": [ {
                  "type": "section",
                  "text": {
                      "type": "mrkdwn",
                      "text": "'${TIMESTAMP}' | Updated router config has been committed"
                  }
              }]
            }' \
    -X POST ${ANSBL_WEBHOOK} > /dev/null 2>&1
}

# Vars
SVC_ACCT=robackup
ROUTER=192.168.11.1
CURRENT_CONFIG=mikrotik.conf.current
#REPO_DIR=~/<something>
PREVIOUS_CONFIG=mikrotik.conf

### MAIN ###

#if [ $(whoami) != '${SVC_ACCT}' ];then
#  echo ""
#  echo "This script must be run as ${SVC_ACCT} user"
#  exit 1
#fi
#
#cd /tmp
#ssh ${SVC_ACCT}@${ROUTER} /export > ${CURRENT_CONFIG}
#compare_configs ${CURRENT_CONFIG} ${PREVIOUS_CONFIG}

#echo "${TIMESTAMP}"
notify_slack_of_change
sleep 3
notify_slack_of_push

