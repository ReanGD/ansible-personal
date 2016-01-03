import socket


pkgs = []

# drivers
if socket.gethostname() == "archhost":
    pkgs += ["mesa", "nvidia"]
else:
    pkgs += ["mesa",
             "xf86-video-intel",
             "lib32-mesa",
             "xf86-input-synaptics",  # touchpad
             "broadcom-wl"]           # wi-fi

# font packages
pkgs += ["fontconfig-ubuntu",
         "cairo-ubuntu",
         "ttf-ms-fonts",
         "ttf-fixedsys-excelsior-linux",
         "ttf-droid",
         "ttf-dejavu",
         "ttf-ubuntu-font-family",
         "adobe-source-code-pro-fonts"]

# terminal
pkgs += ["rxvt-unicode-patched", "urxvt-perls-git", "zsh", "oh-my-zsh-git"]

# system
pkgs += ["grub",
         "polkit",
         "htop",
         "xcursor-aero",
         "pkgfile",    # pkgfile makepkg (get package for makepkg)
         "rsync",
         "kbdd",       # daemon to make per window layout
         "libnotify",  # create notifications message
         "autofs"]

# WM
pkgs += ["xorg-server",
         "xorg-xinit",
         "xorg-server-utils",
         "awesome",
         "vicious",
         "rofi-git",            # run app menu
         "xcursor-aero"]

# login manager
pkgs += ["slim", "slim-themes", "archlinux-themes-slim"]

# net tools
pkgs += ["wget",
         "wpa_supplicant",
         "net-tools",
         "dialog",              # ???
         "wireless_tools",
         "smbclient",
         "nfs-utils",
         "openssh"]

# remote access
pkgs += ["teamviewer"]

# audio
pkgs += ["pulseaudio",
         "pavucontrol",
         "volumeicon"]

# web
pkgs += ["firefox", "firefox-i18n-ru", "flashplugin"]

# cpp
pkgs += ["boost", "clang", "gtest", "zeromq", "valgrind", "cmake"]

# rust
# pkgs += ["rust", "cargo-bin", "rust-racer-git", "rust-src"]
# rust-doc-git

# go
pkgs += ["go"]

# python
pkgs += ["python",
         "python2",
         "python-pip",
         "python2-pip",
         "python-nose",
         "python2-nose",
         "python-jedi",
         "python2-jedi",
         "python-pylint",
         "python2-pylint",
         "flake8",
         "python2-flake8",
         "tk"]

# text editors
pkgs += ["emacs", "vim", "sublime-text-nightly"]

# file managers
pkgs += ["doublecmd-gtk2",
         "transmission-remote-gui-bin",
         "yandex-disk",  # yandex-disk setup/start
         "dropbox"]

# git
pkgs += ["git", "meld"]

# Messengers
pkgs += ["skype"]

# archive program
pkgs += ["p7zip", "unzip", "unrar"]

# media
pkgs += ["shutter",     # screenshots
         "byzanz-git",  # create gif from screen
         "simplescreenrecorder",  # write video from screen
         "gimp",
         "blender",
         "smplayer",
         "deadbeef"]

# office
pkgs += ["llpp"         # pdf viewer
         # "libreoffice-fresh"
         ]

# spell checkers
pkgs += ["enchant", "hunspell-en", "hunspell-ru-aot", "languagetool"]

# android
if socket.gethostname() != "archhost":
    pkgs += ["adb"]

# xorg
pkgs += ["xorg-xfontsel",  # font select
         "xorg-xprop",     # window info (xprop | grep WM_CLASS)
         "xorg-xev",       # keypress info
         "xrectsel"]       # get select region

# VM
pkgs += ["jre7-openjdk", "docker"]

# 3D
pkgs += ["sdl2", "sdl2_image"]

# game
pkgs += ["playonlinux", "minecraft"]

packages = pkgs
ignore_packages = ["yaourt", "package-query", "ansible"]
ignore_groups = ["base", "base-devel"]
