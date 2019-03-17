# global host
pkgs = []
grps = []

is_notebook = host in ["archnote"]
# drivers
pkgs += ["mesa"]

if host == "archhost":
    pkgs += ["nvidia",
             "lib32-nvidia-utils"  # for steam
             ]
elif host == "archnote":
    pkgs += ["bbswitch",
             # "bumblebee",
             # "nvidia",
             "xf86-video-intel",
             "xf86-input-libinput"]  # touchpad

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
         "libnewt",  # external dialog
         "oh-my-zsh-git",
         "zsh-syntax-highlighting",
         "fzf"]

# system
pkgs += ["refind-efi",
         "polkit",
         "gnupg",
         "xcursor-ize-vision",  # a couple of X cursor that similar to Windows 7 cursor.
         "pkgfile",  # pkgfile makepkg (get package for makepkg)
         "pkgcacheclean",  # clean the pacman cache
         "perwindowlayoutd",  # daemon to make per window layout (also exists "kbdd-git")
         "libnotify",  # create notifications message
         "yay",  # AUR package manager
         "ansible",
         "rsync"]

# WM
pkgs += ["xorg-server",
         "xorg-xinit",
         "awesome",
         "rofi",  # run app menu
         "vicious"]

if is_notebook:
    pkgs += ["cinnamon"]

# login manager
pkgs += ["lightdm", "lightdm-gtk-greeter"]

# net tools
pkgs += ["wget",         
         "net-tools",
         "dialog",
         "smbclient",
         "nfs-utils",
         "httpie",
         "openssh",
         "openvpn",
         "openconnect", # for vpn to work
         ]

if is_notebook:
    pkgs += ["connman", "wpa_supplicant"]

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

# programming
pkgs += ["protobuf"]

# cpp
pkgs += ["boost", "clang", "gtest", "zeromq", "valgrind", "cmake", "clion-cmake", "gdb"]

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
         "python-termcolor",
         "python-virtualenv",
         "tk",
         "swig",
         "portaudio",  # for pyaudio and my audio-lib
         ]

# text editors & ide
pkgs += ["emacs", "vim", "sublime-text-dev", "code", "clion"]
if is_notebook:
    pkgs += ["pycharm-community-edition"]
else:
    pkgs += ["pycharm-professional"]

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
pkgs += ["mupdf"  # pdf viewer (analog: llpp-git)
         # "libreoffice-fresh"
         ]

# spell checkers
pkgs += ["enchant", "hunspell-en_US", "hunspell-ru-aot", "languagetool"]

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
pkgs += ["docker", "docker-compose"]

# game
pkgs += ["playonlinux",
        "steam",
        "lib32-libldap",  # for WOT ?
        "minecraft"]

# messengers
pkgs += ["telegram-desktop"]

# groups
grps += ["base", "base-devel"]

packages = pkgs
groups = grps
