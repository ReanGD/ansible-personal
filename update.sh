#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cd $ROOT_DIR
MENU_ID=$(whiptail --clear --title 'Update host' \
--menu "Enter your choice:" 15 60 5 \
	"1" "local" \
	"2" "master" \
	"3" "server" \
	"4" "xnote" \
	"5" "worknote" \
	"6" "Quit" \
	3>&1 1>&2 2>&3)

if [ $? != 0 ]; then
	exit 1
fi

HOST_NAME=""
case $MENU_ID in
  "1")
	HOST_NAME="local"
	;;
  "2")
	HOST_NAME="master"
	;;
  "3")
	HOST_NAME="server"
	;;
  "4")
	HOST_NAME="xnote"
	;;
  "5")
	HOST_NAME="worknote"
	;;
  "6")
	exit 1
	;;
esac

/usr/bin/ansible-playbook update.yml --ask-become-pass --ask-vault-pass --extra-vars "variable_host=${HOST_NAME}" $@
