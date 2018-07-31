#!/bin/bash	

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

BASEURL=http://os.archlinuxarm.org/os/
RPI2=ArchLinuxARM-rpi-2-latest.tar.gz
RPI3=ArchLinuxARM-rpi-3-latest.tar.gz
ARMV7IMG=arch-linux-armv7.img
ARMV8IMG=arch-linux-armv8.img

create_image(){
	NAME=$1
	IMG=$2
	cd ~/tmp
	losetup /dev/loop0 && exit 1 || true
	wget -N $BASEURL$NAME
	truncate -s 1300M $IMG
	losetup /dev/loop0 $IMG
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
	bsdtar -xpf $NAME -C arch-root
	mv arch-root/boot/* arch-boot/
	
	# fix boot
	sed -i 's/gpu_mem=64/gpu_mem=16/' arch-boot/config.txt	
	sed -i "s/ defaults / defaults,noatime /" arch-root/etc/fstab
	sed -i "s/mmcblk0p1/sda1/" arch-root/etc/fstab
	if [ $NAME = $RPI2 ]; then
		sed -i "s/mmcblk0p2/sda2/" arch-boot/cmdline.txt
	fi

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
	echo "Finish. Image path = ~/tmp/$IMG"
}

if [ $EUID != 0 ]; then
    sudo "$0" "$@"
    exit $?
fi

retval=$(whiptail --clear --title 'Scenarios for raspberry Pi 3'\
	--menu "Enter your choice:" 15 60 3 \
		"1" "Create image for ARMv7" \
		"2" "Create image for ARMv8" \
		"3" "Quit" \
		3>&1 1>&2 2>&3)

if [ $? != 0 ]; then
	exit 1
fi

case $retval in
  "1")
	create_image "$RPI2" "$ARMV7IMG"
	;;
  "2")
	create_image "$RPI3" "$ARMV8IMG"
	;;
  "3")
	exit 1
	;;
esac


