#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $ROOT_DIR

MENU_ID=$(whiptail --clear --title 'Get info about host' \
--menu "Enter your choice:" 15 60 6 \
	"1" "archhost" \
	"2" "archnote" \
	"3" "archsrv" \
	"4" "hass" \
	"5" "kvmtest" \
	"6" "Quit" \
	3>&1 1>&2 2>&3)

if [ $? != 0 ]; then
	exit 1
fi

HOST_NAME=""
case $MENU_ID in
  "1")
	HOST_NAME="archhost"
	;;
  "2")
	HOST_NAME="archnote"
	;;
  "3")
	HOST_NAME="archsrv"
	;;
  "4")
	HOST_NAME="hass"
	;;
  "5")
	HOST_NAME="kvmtest"
	;;
  "6")
	exit 1
	;;
esac

/usr/bin/ansible-playbook info.yml --ask-become-pass --extra-vars "variable_host=${HOST_NAME}" $@
