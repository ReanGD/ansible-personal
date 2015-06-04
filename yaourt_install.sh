#!/bin/bash

yaourt -S --needed --noconfirm curl

rm -rf /tmp/yaourt
mkdir -p /tmp/yaourt

cd /tmp/yaourt
curl -O https://aur.archlinux.org/packages/pa/package-query/package-query.tar.gz
tar zxvf package-query.tar.gz
cd /tmp/yaourt/package-query
makepkg -si --needed

cd /tmp/yaourt/
curl -O https://aur.archlinux.org/packages/ya/yaourt/yaourt.tar.gz
tar zxvf yaourt.tar.gz
cd /tmp/yaourt/yaourt
makepkg -si --needed

rm -rf /tmp/yaourt
