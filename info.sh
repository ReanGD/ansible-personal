#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $ROOT_DIR

MENU_ID=$(whiptail --clear --title 'Get info about host' \
--menu "Enter your choice:" 15 60 6 \
	"1" "master" \
	"2" "xnote" \
	"3" "server" \
	"4" "hass" \
	"5" "worknote" \
	"6" "kvmtest" \
	"7" "Quit" \
	3>&1 1>&2 2>&3)

if [ $? != 0 ]; then
	exit 1
fi

HOST_NAME=""
case $MENU_ID in
  "1")
	HOST_NAME="master"
	;;
  "2")
	HOST_NAME="xnote"
	;;
  "3")
	HOST_NAME="server"
	;;
  "4")
	HOST_NAME="hass"
	;;
  "5")
	HOST_NAME="worknote"
	;;
  "6")
	HOST_NAME="kvmtest"
	;;
  "7")
	exit 1
	;;
esac

/usr/bin/ansible-playbook info.yml --ask-become-pass --extra-vars "variable_host=${HOST_NAME}" $@
