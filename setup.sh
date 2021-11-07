#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
MENU_ID=$1

run_with_sudo(){
	if [ $EUID != 0 ]; then
		sudo "$0" "$MENU_ID"
		exit $?
	fi
}

function server {
    echo "server" $1
    if [[ $1 = "full" ]]
    then
        sgdisk --zap-all /dev/sda
        sgdisk --new=1:0:+512M --typecode=1:ef00 --change-name=1:"boot" /dev/sda
        sgdisk --largest-new=2 --typecode=2:8300 --change-name=2:"root" /dev/sda
        sgdisk --zap-all /dev/sdb
        sgdisk --largest-new=1 --typecode=1:8300 --change-name=1:"data" /dev/sdb
        sgdisk --zap-all /dev/sdc
        sgdisk --largest-new=1 --typecode=1:8300 --change-name=1:"backup" /dev/sdc
    fi

    mkfs.fat -F32 /dev/sda1
    mkfs.ext4 -L "root" /dev/sda2
    mkfs.btrfs -L "data" /dev/sdb1
    mkfs.ext4 -L "backup" /dev/sdc1

    mount /dev/sda2 /mnt

    mkdir -p /mnt/boot/efi
    mount /dev/sda1 /mnt/boot/efi

    mkdir -p /mnt/data/main
    mount /dev/sdb1 /mnt/data/main

    mkdir -p /mnt/backup/local
    mount /dev/sdc1 /mnt/backup/local
}

function master {
    echo "master" $1
    if [[ $1 = "full" ]]
    then
        sgdisk --zap-all /dev/nvme0n1
        sgdisk --new=1:0:+512M --typecode=1:ef00 --change-name=1:"boot" /dev/nvme0n1
        sgdisk --largest-new=2 --typecode=2:8300 --change-name=2:"root" /dev/nvme0n1
    fi
    # add hdd format and mount (/disk0)
    mkfs.fat -F32 /dev/nvme0n1p1
    mkfs.ext4 -L "root" /dev/nvme0n1p2

    mount /dev/nvme0n1p2 /mnt

    mkdir -p /mnt/boot/efi
    mount /dev/nvme0n1p1 /mnt/boot/efi
}

function xnote {
    echo "xnote" $1
    if [[ $1 = "full" ]]
    then
        sgdisk --zap-all /dev/nvme0n1
        sgdisk --new=1:0:+512M --typecode=1:ef00 --change-name=1:"boot" /dev/nvme0n1
        sgdisk --largest-new=2 --typecode=2:8300 --change-name=2:"root" /dev/nvme0n1
    fi

    mkfs.fat -F32 /dev/nvme0n1p1
    mkfs.ext4 -L "root" /dev/nvme0n1p2

    mount /dev/nvme0n1p2 /mnt

    mkdir -p /mnt/boot/efi
    mount /dev/nvme0n1p1 /mnt/boot/efi
}

function worknote {
    echo "worknote" $1
    if [[ $1 = "full" ]]
    then
        sgdisk --zap-all /dev/sda
        sgdisk --new=1:0:+512M --typecode=1:ef00 --change-name=1:"boot" /dev/sda
        sgdisk --new=2:0:+150GiB --typecode=2:8300 --change-name=2:"root" /dev/sda
        sgdisk --largest-new=3 --typecode=3:8302 --change-name=3:"home" /dev/sda

        cryptsetup luksFormat /dev/sda3
        cryptsetup open /dev/sda3 home
    fi

    mkfs.fat -F32 /dev/sda1
    mkfs.ext4 -L "root" /dev/sda2
    mkfs.ext4 -L "home" /dev/mapper/home

    mount /dev/sda2 /mnt

    mkdir -p /mnt/boot/efi
    mount /dev/sda1 /mnt/boot/efi

    mkdir -p /mnt/home
    mount /dev/mapper/home /mnt/home
}

function kvmtest {
    echo "kvmtest" $1
    if [[ $1 = "full" ]]
    then
        sgdisk --zap-all /dev/vda
        sgdisk --new=1:0:+512M --typecode=1:ef00 --change-name=1:"boot" /dev/vda
        sgdisk --new=2:0:+25GiB --typecode=2:8300 --change-name=2:"root" /dev/vda
        sgdisk --largest-new=3 --typecode=3:8302 --change-name=3:"home" /dev/vda
        cryptsetup luksFormat /dev/vda3
        cryptsetup open /dev/vda3 home
    fi

    mkfs.fat -F32 /dev/vda1
    mkfs.ext4 -L "root" /dev/vda2
    mkfs.ext4 -L "home" /dev/mapper/home

    mount /dev/vda2 /mnt

    mkdir -p /mnt/boot/efi
    mount /dev/vda1 /mnt/boot/efi

    mkdir -p /mnt/home
    mount /dev/mapper/home /mnt/home
}

function setup_base {
    BOARD_NAME=$(cat /sys/class/dmi/id/product_name)
    case $BOARD_NAME in
    'MS-7978')
        FUNC="server"
        ;;
    'MS-7C90')
        FUNC="master"
        ;;
    'TM1613')
        FUNC="xnote"
        ;;
    'Latitude 5480')
        FUNC="worknote"
        ;;
    'Standard PC (Q35 + ICH9, 2009)')
        FUNC="kvmtest"
        ;;
    *)
        echo 'Unknown product name'
        exit 1
        ;;
    esac

    DISTRO_NAME=$(cat /etc/os-release | grep "^ID=" | cut -d'=' -f2-)
    case $DISTRO_NAME in
    'arch')
        echo 'distro = arch'
        echo 'Server = http://mirror.yandex.ru/archlinux/$repo/os/$arch' > /etc/pacman.d/mirrorlist
        pacman -Sy dialog --noconfirm
        ;;
    'archarm')
        echo 'distro = archarm'
        ;;
    *)
        echo 'Unknown distro name'
        exit 1
        ;;
    esac

    dialog --title 'Install' --clear --defaultno --yesno 'Recreate partition table?' 10 40
    case "$?" in
    '0')
        clear
        eval ${FUNC} 'full'
        ;;
    '1')
        clear
        eval ${FUNC} 'part'
        ;;
    '-1')
        clear
        echo 'Unknown choice'
        exit 1
        ;;
    esac

    read -n 1 -s -p "Press any key to continue"
    case $DISTRO_NAME in
    'arch')
        pacstrap /mnt base base-devel linux linux-firmware nano git ansible
        genfstab -U -p /mnt >> /mnt/etc/fstab
        arch-chroot /mnt git clone git://github.com/ReanGD/ansible-personal.git /etc/ansible-personal
        arch-chroot /mnt /etc/ansible-personal/setup.sh ansible
        ;;
    'archarm')
        pacstrap /mnt base base-devel linux linux-firmware nano git ansible
        genfstab -U -p /mnt >> /mnt/etc/fstab
        arch-chroot /mnt git clone git://github.com/ReanGD/ansible-personal.git /etc/ansible-personal
        arch-chroot /mnt /etc/ansible-personal/setup.sh ansible
        ;;
    esac

    # umount -R /mnt
}

case $MENU_ID in
  "ansible")
    cd $ROOT_DIR
    /usr/bin/ansible-playbook setup.yml --ask-become-pass --ask-vault-pass
	;;
  * )
    run_with_sudo
	setup_base
	;;
esac
