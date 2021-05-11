#!/usr/bin/sh 

usage() {
  echo ""
  echo "Usage: push-ssh-key.sh <server ip/name>"
  echo ""
}

### MAIN ###

SERVER=$1

if [ $# -ne 1 ]
then
  echo ""
  echo "Must give a server ip/name"
  usage
fi

if [ $(whoami) != 'ansible' ]
then
  echo "This script must be run as ansible user"
  exit 1
fi

ssh-copy-id -i ~/.ssh/id_rsa.pub ansible@${SERVER}
