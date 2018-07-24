#!/bin/bash

function archhost {
    echo "archhost" $1
    if [[ $1 = "full" ]]
    then
        sgdisk -Z /dev/sda
        sgdisk -n 0:0:+550M -t 0:ef00 -c 0:"boot" /dev/sda
        sgdisk -n 0:0:0 -t 0:8300 -c 0:"root" /dev/sda
    fi

    mkfs.fat -F32 /dev/sda1
    mkfs.ext4 /dev/sda2

    mount /dev/sda2 /mnt
    mkdir -p /mnt/boot/efi
    mount /dev/sda1 /mnt/boot/efi
}

function archnote {
    echo "archnote" $1
    if [[ $1 = "full" ]]
    then
        sgdisk -Z /dev/nvme0n1
        sgdisk -n 0:0:+450M -t 0:ef00 -c 0:"boot" /dev/nvme0n1
        sgdisk -n 0:0:0 -t 0:8300 -c 0:"root" /dev/nvme0n1
    fi

    mkfs.fat -F32 /dev/nvme0n1p1
    mkfs.ext4 /dev/nvme0n1p2

    mount /dev/nvme0n1p2 /mnt
    mkdir -p /mnt/boot/efi
    mount /dev/nvme0n1p1 /mnt/boot/efi
}


BOARD_NAME=$(cat /sys/class/dmi/id/product_name)
case $BOARD_NAME in
'MS-7978')
    FUNC="archhost"
    ;;
'TM1613')
    FUNC="archnote"
    ;;
*)
    echo 'Unknown product name'
    exit 1
    ;;
esac

umount -R /mnt
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

echo 'Server = http://mirror.yandex.ru/archlinux/$repo/os/$arch' > /etc/pacman.d/mirrorlist
pacstrap /mnt base base-devel git ansible python2
genfstab -U -p /mnt >> /mnt/etc/fstab
arch-chroot /mnt git clone git://github.com/ReanGD/ansible-personal.git /etc/ansible-personal
arch-chroot /mnt /etc/ansible-personal/root.sh
umount -R /mnt
