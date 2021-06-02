#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $ROOT_DIR

MENU_ID=$(whiptail --clear --title 'Get info about host' \
--menu "Enter your choice:" 15 60 7 \
	"1" "archhost" \
	"2" "master" \
	"3" "xnote" \
	"4" "archsrv" \
	"5" "hass" \
	"6" "worknote" \
	"7" "kvmtest" \
	"8" "Quit" \
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
	HOST_NAME="master"
	;;
  "3")
	HOST_NAME="xnote"
	;;
  "4")
	HOST_NAME="archsrv"
	;;
  "5")
	HOST_NAME="hass"
	;;
  "6")
	HOST_NAME="worknote"
	;;
  "7")
	HOST_NAME="kvmtest"
	;;
  "8")
	exit 1
	;;
esac

/usr/bin/ansible-playbook info.yml --ask-become-pass --extra-vars "variable_host=${HOST_NAME}" $@
