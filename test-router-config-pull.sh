#!/bin/bash

compare_configs() {
  C1=$1
  C2=$2

  # Remove 1st line
  tail -n +2 /tmp/${C1} > /tmp/${C1}.1d
  tail -n +2 /tmp/${C2} > /tmp/${C2}.1d

  diff ${C1}.1d ${C2}.1d > /dev/null 2>&1
  if [ $? != 0 ];then
    notify_slack_of_changes
    push_new_config "${C1}"
  fi
  rm /tmp/${C1}.1d /tmp/${C2}.1d
}

notify_slack_of_changes() {
  TIMESTAMP=$(date "+%Y-%m-%dT%H:%M:%S.%6NZ")
  curl \
    -H "Content-type: application/json" \
    --data '{
      "channel": "ansible-notifications",
      "blocks": [{
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "'${TIMESTAMP}' | Router config has been updated"
        }
      }]
    }' \
    -X POST ${ANSBL_WEBHOOK} > /dev/null 2>&1 
  sleep 1
}

push_new_config() {
  NEW_CONFIG=$1

  cd ${REPO_DIR}
  cp /tmp/${NEW_CONFIG} .
  git add ${NEW_CONFIG}; git commit -m "Changes made to mikrotik.conf"; git push origin
  notify_slack_of_push
}

notify_slack_of_push() {
  TIMESTAMP=$(date "+%Y-%m-%dT%H:%M:%S.%6NZ")
  curl \
    -H "Content-type: application/json" \
    --data '{
      "channel": "ansible-notifications",
      "blocks": [{
        "type": "section",
        "text": {
          "type": "mrkdwn",
          "text": "'${TIMESTAMP}' | Updated router config has been committed"
        }
      }]
    }' \
    -X POST ${ANSBL_WEBHOOK} > /dev/null 2>&1 
  sleep 1
}

# Vars
SVC_ACCT=robackup
ROUTER=192.168.11.1
CURRENT_CONFIG=mikrotik.conf.current
REPO_DIR=~/projects/ans
PREVIOUS_CONFIG=mikrotik.conf

### MAIN ###

cd /tmp
ssh ${SVC_ACCT}@${ROUTER} /export hide-sensitive > ${CURRENT_CONFIG}
#compare_configs ${CURRENT_CONFIG} ${PREVIOUS_CONFIG}

