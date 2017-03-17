# global host
pkgs = []


# drivers
pkgs += ["mesa"]
if host in ["archhost", "archnote"]:
   pkgs += ["nvidia"]
   # sudo pacman -S lib32-nvidia-utils lib32-nvidia-libgl

if host == "archmini":
    pkgs += ["xf86-video-intel",
             "lib32-mesa",
             "xf86-input-synaptics",  # touchpad
             "broadcom-wl"]           # wi-fi


# monitoring
pkgs += ["iftop",         # network monitor
         "htop",          # process monitor
         "iotop",         # disk monitor
         "hddtemp",       # disk temperature
         "smartmontools"]

if host == "archhost":
   pkgs += ["apcupsd"]    # UPS


# font packages
pkgs += ["ttf-ms-fonts",
         "ttf-tahoma",
         "ttf-vista-fonts",
         "ttf-fixedsys-excelsior-linux",
         "ttf-droid",
         "ttf-dejavu",
         "ttf-ubuntu-font-family",
         "adobe-source-code-pro-fonts"]

# terminal
pkgs += ["rxvt-unicode-patched", "urxvt-perls", "zsh", "oh-my-zsh-git", "zsh-syntax-highlighting", "fzf"]

# system
pkgs += ["grub",
         "polkit",
         "xcursor-ize-vision",
         "pkgfile",        # pkgfile makepkg (get package for makepkg)
         "pkgcacheclean",  # clean the pacman cache         
         "kbdd-git",       # daemon to make per window layout
         "libnotify",      # create notifications message
         "autofs",         # automounter (nfs, samba, etc)
         # "pacaur",         # AUR package manager
         "rsync"]

# WM
pkgs += ["xorg-server",
         "xorg-xinit",
         # "xorg-server-utils", removed
         "awesome",
         "rofi-git",            # run app menu
         "vicious"]

# login manager
pkgs += ["lightdm", "lightdm-gtk-greeter"]

# net tools
pkgs += ["wget",
         "wpa_supplicant",
         "net-tools",
         "dialog",
         "smbclient",
         "nfs-utils",
         "openssh"]

# remote access
# pkgs += ["teamviewer"]

# audio
pkgs += ["pulseaudio",
         "pavucontrol",
         "volumeicon"]

# web
pkgs += ["firefox",
         "firefox-i18n-ru",
         "flashplugin"]

# cpp
pkgs += ["boost", "clang", "gtest", "zeromq", "valgrind", "cmake"]

# rust
pkgs += ["rust", "cargo", "rust-src", "rust-racer"]
# rust-doc-git

# sql
pkgs += ["sqlite-analyzer"]

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
         "python-pytest",
         "python-virtualenv",
         "tk"]

# text editors
pkgs += ["emacs", "vim", "sublime-text-dev", "pycharm-community"]

# file managers
pkgs += ["doublecmd-gtk2",
         "transmission-remote-gui-bin",
         "yandex-disk",  # yandex-disk setup/start
         "dropbox"]

# git
pkgs += ["git",
         "icdiff",  # console diff
         "meld"]

# messengers
pkgs += ["skypeforlinux-bin"]

# archive program
pkgs += ["p7zip", "unzip", "unrar"]

# media
pkgs += ["shutter",     # screenshots
         "byzanz-git",  # create gif from screen
         "viewnior",    # image viewer
         "simplescreenrecorder",  # write video from screen
         "gimp",
         "blender",
         "smplayer",
         "deadbeef"]

# office
pkgs += ["mupdf"   # pdf viewer
         #"llpp-git"  # pdf viewer
         # "libreoffice-fresh"
         ]

# spell checkers
pkgs += ["enchant", "hunspell-en", "hunspell-ru-aot", "languagetool"]

# android
# if host == "archhost":
#     pkgs += ["adb"]
# if host == "archmini":
#     pkgs += ["android-studio"]

# xorg
pkgs += ["xorg-xfontsel",  # font select
         "xorg-xprop",     # window info (xprop | grep WM_CLASS)
         "xorg-xev",       # keypress info
         "xorg-xwininfo",  # select window
         "xrectsel"]       # get select region

# VM
pkgs += ["jre7-openjdk", "docker", "docker-compose"]

# 3D
pkgs += ["sdl2", "sdl2_image"]

# game
pkgs += ["playonlinux",
         "lib32-libldap",  # for WOT ?
         "minecraft"]

packages = pkgs
ignore_packages = ["yaourt", "package-query", "ansible"]
ignore_groups = ["base", "base-devel"]
