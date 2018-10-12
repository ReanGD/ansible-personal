#!/bin/bash	

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
MENU_ID=$1

run_with_sudo(){
	if [ $EUID != 0 ]; then
		sudo "$0" "$MENU_ID"
		exit $?
	fi
}

fix_image(){
	SD_PATH=$(whiptail --inputbox "Path to sd card" 8 78 /dev/sde2 --title "Path Dialog" 3>&1 1>&2 2>&3)
	if [ $? != 0 ]; then
		exit 1
	fi
	cd ~/tmp
	mkdir -p partition
	mount $SD_PATH partition

	# ssh config
	echo 'PermitRootLogin yes' > partition/etc/ssh/sshd_config
	echo 'PasswordAuthentication no' >> partition/etc/ssh/sshd_config
	mkdir -p partition/root/.ssh/
	ssh-keygen -y -f ~/.ssh/respeaker > partition/root/.ssh/authorized_keys
	chmod 0600 partition/root/.ssh/authorized_keys

	# sudo config
	cp -rf $ROOT_DIR/files/respeaker/etc/sudoers partition/etc/sudoers
	chmod 0440 partition/etc/sudoers

	# network config
	cp -rf $ROOT_DIR/files/respeaker/etc/systemd/network/wired.network partition/etc/systemd/network/wired.network
	chmod 0755 partition/etc/systemd/network/wired.network

	# install script
	cp -rf $ROOT_DIR/files/respeaker/bin/install partition/bin/install
	chmod +x partition/bin/install

	umount partition
	rm -rf partition
	echo "Finish."
}

main_menu(){
	MENU_ID=$(whiptail --clear --title 'Scenarios for respeaker'\
	--menu "Enter your choice:" 15 60 4 \
		"1" "Fix image on SD card" \
		"2" "Ansible base install" \
		"3" "Ansible update" \
		"4" "Quit" \
		3>&1 1>&2 2>&3)

	if [ $? != 0 ]; then
		exit 1
	fi
}

if [ -z "$MENU_ID" ]; then
   main_menu
fi

case $MENU_ID in
  "1")
	run_with_sudo
	fix_image
	;;
  "2")
	cd $ROOT_DIR
	/usr/bin/ansible-playbook tasks/respeaker/main_base.yml --ask-become-pass --ask-vault-pass
	;;
  "3")
	cd $ROOT_DIR
	/usr/bin/ansible-playbook tasks/respeaker/main_update.yml --ask-become-pass --ask-vault-pass
	;;
  "4")
	exit 1
	;;
esac
