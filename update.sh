#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cd $ROOT_DIR
MENU_ID=$(whiptail --clear --title 'Get info about host' \
--menu "Enter your choice:" 15 60 6 \
	"1" "local" \
	"2" "archhost" \
	"3" "master" \
	"4" "xnote" \
	"5" "archsrv" \
	"6" "worknote" \
	"7" "Quit" \
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
	HOST_NAME="archhost"
	;;
  "3")
	HOST_NAME="master"
	;;
  "4")
	HOST_NAME="xnote"
	;;
  "5")
	HOST_NAME="archsrv"
	;;
  "6")
	HOST_NAME="worknote"
	;;
  "7")
	exit 1
	;;
esac

/usr/bin/ansible-playbook update.yml --ask-become-pass --ask-vault-pass --extra-vars "variable_host=${HOST_NAME}" $@
