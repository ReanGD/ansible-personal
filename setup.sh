#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
MENU_ID=$1

run_with_sudo(){
	if [ $EUID != 0 ]; then
		sudo "$0" "$MENU_ID"
		exit $?
	fi
}

function archhost {
    echo "archhost" $1
    if [[ $1 = "full" ]]
    then
        sgdisk -Z /dev/sda
        sgdisk -n 0:0:+512M -t 0:ef00 -c 0:"boot" /dev/sda
        sgdisk -n 0:0:0 -t 0:8300 -c 0:"root" /dev/sda
    fi
    # add hdd format and mount (/disk0)
    mkfs.fat -F32 /dev/sda1
    mkfs.ext4 /dev/sda2

    mount /dev/sda2 /mnt
    mkdir -p /mnt/boot/efi
    mount /dev/sda1 /mnt/boot/efi
}

function master {
    echo "master" $1
    if [[ $1 = "full" ]]
    then
        sgdisk -Z /dev/nvme0n1
        sgdisk -n 0:0:+512M -t 0:ef00 -c 0:"boot" /dev/nvme0n1
        sgdisk -n 0:0:0 -t 0:8300 -c 0:"root" /dev/nvme0n1
    fi
    # add hdd format and mount (/disk0)
    mkfs.fat -F32 /dev/nvme0n1p1
    mkfs.ext4 /dev/nvme0n1p2

    mount /dev/nvme0n1p2 /mnt
    mkdir -p /mnt/boot/efi
    mount /dev/nvme0n1p1 /mnt/boot/efi
}

function xnote {
    echo "xnote" $1
    if [[ $1 = "full" ]]
    then
        sgdisk -Z /dev/nvme0n1
        sgdisk -n 0:0:+512M -t 0:ef00 -c 0:"boot" /dev/nvme0n1
        sgdisk -n 0:0:0 -t 0:8300 -c 0:"root" /dev/nvme0n1
    fi

    mkfs.fat -F32 /dev/nvme0n1p1
    mkfs.ext4 /dev/nvme0n1p2

    mount /dev/nvme0n1p2 /mnt
    mkdir -p /mnt/boot/efi
    mount /dev/nvme0n1p1 /mnt/boot/efi
}

function archsrv {
    echo "archsrv" $1
    if [[ $1 = "full" ]]
    then
        sgdisk -Z /dev/sda
        sgdisk -n 0:0:+512M -t 0:ef00 -c 0:"boot" /dev/sda
        sgdisk -n 0:0:0 -t 0:8300 -c 0:"root" /dev/sda
    fi

    mkfs.fat -F32 /dev/sda1
    mkfs.ext4 /dev/sda2

    mount /dev/sda2 /mnt
    mkdir -p /mnt/boot/efi
    mount /dev/sda1 /mnt/boot/efi
}

function worknote {
    echo "worknote" $1
    if [[ $1 = "full" ]]
    then
        sgdisk -Z /dev/sda
        sgdisk -n 0:0:+512M -t 0:ef00 -c 0:"boot" /dev/sda
        sgdisk -n 0:0:+150GiB -t 0:8300 -c 0:"root" /dev/sda
        sgdisk -n 0:0:0 -t 0:8302 -c 0:"home" /dev/sda

        cryptsetup luksFormat /dev/sda3
        cryptsetup open /dev/sda3 home
    fi

    mkfs.fat -F32 /dev/sda1
    mkfs.ext4 /dev/sda2
    mkfs.ext4 /dev/mapper/home

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
        sgdisk -Z /dev/vda
        sgdisk -n 0:0:+512M -t 0:ef00 -c 0:"boot" /dev/vda
        sgdisk -n 0:0:+25GiB -t 0:8300 -c 0:"root" /dev/vda
        sgdisk -n 0:0:0 -t 0:8302 -c 0:"home" /dev/vda
        cryptsetup luksFormat /dev/vda3
        cryptsetup open /dev/vda3 home
    fi

    mkfs.fat -F32 /dev/vda1
    mkfs.ext4 /dev/vda2
    mkfs.ext4 /dev/mapper/home

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
        FUNC="archhost"
        ;;
    'MS-7C90')
        FUNC="master"
        ;;
    'TM1613')
        FUNC="xnote"
        ;;
    'System Product Name')
        FUNC="archsrv"
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
        ;;
    'archarm')
        echo 'distro = archarm'
        ;;
    'manjaro')
        echo 'distro = manjaro'
        echo 'Server = http://mirror.truenetwork.ru/manjaro/stable/$repo/$arch' > /etc/pacman.d/mirrorlist
        pacman -Sy gptfdisk dialog --noconfirm
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
    'manjaro')
        basestrap /mnt base base-devel linux512 linux-firmware nano git ansible
        fstabgen -U -p /mnt >> /mnt/etc/fstab
        manjaro-chroot /mnt git clone git://github.com/ReanGD/ansible-personal.git /etc/ansible-personal
        manjaro-chroot /mnt /etc/ansible-personal/setup.sh ansible
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
