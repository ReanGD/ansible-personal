#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
MENU_ID=$1

run_with_sudo(){
	if [ $EUID != 0 ]; then
		sudo -E "$0" "$MENU_ID"
		exit $?
	fi
}

create_image(){
	BASEURL="http://os.archlinuxarm.org/os/"
	TAR_FILE_NAME="ArchLinuxARM-rpi-armv7-latest.tar.gz"
	IMG_FILE_NAME="arch-linux-armv7.img"
	cd ~/tmp
	losetup /dev/loop0 && exit 1 || true
	wget -N $BASEURL$TAR_FILE_NAME
	truncate -s 1500M $IMG_FILE_NAME
	losetup /dev/loop0 $IMG_FILE_NAME
	parted -s /dev/loop0 mklabel msdos
	parted -s /dev/loop0 unit MiB mkpart primary fat32 -- 1 100
	parted -s /dev/loop0 set 1 boot on
	parted -s /dev/loop0 unit MiB mkpart primary ext2 -- 100 -1
	parted -s /dev/loop0 print
	mkfs.vfat -n SYSTEM /dev/loop0p1
	mkfs.ext4 -L root -b 4096 -E stride=4,stripe_width=1024 /dev/loop0p2
	mkdir -p arch-boot
	mount /dev/loop0p1 arch-boot
	mkdir -p arch-root
	mount /dev/loop0p2 arch-root
	bsdtar -xpf $TAR_FILE_NAME -C arch-root

	mv arch-root/boot/* arch-boot/

	# fix boot
	sed -i 's/gpu_mem=64/gpu_mem=16/' arch-boot/config.txt
	sed -i "s/ defaults / defaults,noatime /" arch-root/etc/fstab
	sed -i "s/mmcblk0p1/sda1/" arch-root/etc/fstab
	sed -i "s/mmcblk0p2/sda2/" arch-boot/cmdline.txt

	# ssh config
	echo 'PermitRootLogin yes' > arch-root/etc/ssh/sshd_config
	echo 'PasswordAuthentication no' >> arch-root/etc/ssh/sshd_config
	mkdir arch-root/root/.ssh/
	ssh-keygen -y -f ~/.ssh/hass > arch-root/root/.ssh/authorized_keys
	chmod 0600 arch-root/root/.ssh/authorized_keys

	# sudo config
	cp $ROOT_DIR/files/hass/etc/sudoers arch-root/etc/sudoers
	chmod 0440 arch-root/etc/sudoers

	# install script
	cp $ROOT_DIR/files/hass/bin/install arch-root/bin/install
	chmod +x arch-root/bin/install

	umount arch-boot arch-root
	rm -rf arch-boot arch-root
	losetup -d /dev/loop0
	echo "Finish. Image path = ~/tmp/$IMG_FILE_NAME"
}

main_menu(){
	MENU_ID=$(whiptail --clear --title 'Scenarios for raspberry Pi 3'\
	--menu "Enter your choice:" 15 60 6 \
		"1" "Ansible update" \
		"2" "Ansible copy settings to local" \
		"3" "Ansible base install" \
		"4" "Create image for ARMv7" \
		"5" "Quit" \
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
	cd $ROOT_DIR
	/usr/bin/ansible-playbook hass_maintenance.yml --ask-become-pass --ask-vault-pass --extra-vars "is_hass_update=True" $@
	;;
  "2")
	cd $ROOT_DIR
	/usr/bin/ansible-playbook hass_maintenance.yml --extra-vars "is_hass_copy=True" $@
	;;
  "3")
	cd $ROOT_DIR
	/usr/bin/ansible-playbook setup.yml --ask-become-pass --ask-vault-pass --extra-vars "variable_host=hass is_chroot_param=False" $@
	;;
  "4")
	run_with_sudo
	create_image
	;;
  "5")
	exit 1
	;;
esac
