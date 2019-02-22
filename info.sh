#!/bin/bash	

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
cd $ROOT_DIR

MENU_ID=$(whiptail --clear --title 'Get info about host' \
--menu "Enter your choice:" 15 60 4 \
	"1" "archhost" \
	"2" "archnote" \
	"3" "archsrv" \
	"4" "Quit" \
	3>&1 1>&2 2>&3)

if [ $? != 0 ]; then
	exit 1
fi

case $MENU_ID in
  "1")
	/usr/bin/ansible-playbook info.yml --ask-become-pass --extra-vars "variable_host=archhost" $@
	;;
  "2")
	/usr/bin/ansible-playbook info.yml --ask-become-pass --extra-vars "variable_host=archnote" $@
	;;
  "3")
	/usr/bin/ansible-playbook info.yml --ask-become-pass --extra-vars "variable_host=archsrv" $@
	;;
  "4")
	exit 1
	;;
esac
