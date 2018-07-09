# global host
pkgs = []
grps = []

is_notebook = host in ["archmini", "archnote"]
# drivers
pkgs += ["mesa"]

if host == "archhost":
    pkgs += ["nvidia"]  # lib32-nvidia-utils lib32-nvidia-libgl
elif host == "archnote":
    pkgs += ["bbswitch",
             # "bumblebee",
             # "nvidia",
             "xf86-video-intel",
             "xf86-input-libinput"]  # touchpad
elif host == "archmini":
    pkgs += ["xf86-video-intel",
             "lib32-mesa",
             "xf86-input-synaptics",  # touchpad
             "broadcom-wl"]  # wi-fi

# monitoring
pkgs += ["iftop",  # network monitor
         "htop",  # process monitor
         "iotop",  # disk monitor
         "hddtemp",  # disk temperature
         "smartmontools"]

if host == "archhost":
    pkgs += ["apcupsd"]  # UPS
elif is_notebook:
    pkgs += ["powertop"]

# font packages
pkgs += ["ttf-ms-fonts",
         "ttf-tahoma",
         # "ttf-vista-fonts",
         "ttf-fixedsys-excelsior-linux",
         "ttf-droid",
         "ttf-dejavu",
         "ttf-ubuntu-font-family",
         "adobe-source-code-pro-fonts"]

# terminal
pkgs += ["urxvt-perls",
         "zsh",
         "oh-my-zsh-git",
         "zsh-syntax-highlighting",
         "fzf"]

# system
pkgs += ["refind-efi",
         "polkit",
         "gnupg",
         "xcursor-ize-vision",
         "pkgfile",  # pkgfile makepkg (get package for makepkg)
         "pkgcacheclean",  # clean the pacman cache
         "perwindowlayoutd",  # daemon to make per window layout (also exists "kbdd-git")
         "libnotify",  # create notifications message
         "autofs",  # automounter (nfs, samba, etc)
         "aurman",  # AUR package manager
         "rsync"]

# WM
pkgs += ["xorg-server",
         "xorg-xinit",
         "awesome",
         "rofi",  # run app menu
         "vicious"]

if is_notebook:
    grps += ["mate"]

# login manager
pkgs += ["lightdm", "lightdm-webkit2-greeter", "lightdm-webkit2-theme-material2", "lightdm-gtk-greeter"]

# net tools
pkgs += ["wget",
         "wpa_supplicant",
         "net-tools",
         "dialog",
         "connman",
         "smbclient",
         "nfs-utils",
         "httpie",
         "openssh",
         "openvpn",
         ]

# remote access
# pkgs += ["teamviewer"]

# audio
pkgs += ["pulseaudio",
         "pavucontrol",
         "volumeicon"]

# web
pkgs += ["firefox",
         "firefox-i18n-ru",
         "flashplugin",
         "tor-browser-ru",
         "google-chrome",
         ]

# cpp
pkgs += ["boost", "clang", "gtest", "zeromq", "valgrind", "cmake", "gdb"]

# rust
# pkgs += ["rust", "cargo", "rust-src", "rust-racer"]
# rust-doc-git

# 3D for rust
# pkgs += ["sdl2", "sdl2_image"]

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
         "flake8",
         "python-pytest",
         "python-virtualenv",
         "tk",
         ]

# text editors & ide
pkgs += ["emacs", "vim", "sublime-text-dev", "clion", "pycharm-professional"]

# file managers
pkgs += ["doublecmd-gtk2",
         "fsearch-git",
         "transmission-remote-gui-bin",
         "yandex-disk",  # yandex-disk setup/start
         "dropbox"]

# git
pkgs += ["git",
         "icdiff",  # console diff
         "meld"]

# archive program
pkgs += ["p7zip", "unzip", "unrar"]

# media
pkgs += ["byzanz-git",  # create gif from screen
         "viewnior",  # image viewer
         "simplescreenrecorder",  # write video from screen
         "gimp",
         "blender",
         "smplayer",
         "deadbeef"]

# office
pkgs += ["mupdf"  # pdf viewer
         # "llpp-git"  # pdf viewer
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
         "xorg-xprop",  # window info (xprop | grep WM_CLASS)
         "xorg-xev",  # keypress info
         "xorg-xwininfo",  # select window
         "xrectsel"]  # get select region

if is_notebook:
    pkgs += ["xorg-xbacklight"]  # backlight control application (xbacklight -set 40)

# VM
pkgs += ["jre7-openjdk", "docker", "docker-compose"]

# game
pkgs += ["playonlinux",
        "steam",
        "lib32-libldap",  # for WOT ?
        "minecraft"]

packages = pkgs
groups = grps
ignore_packages = ["yaourt", "ansible"]
ignore_groups = ["base", "base-devel"]
