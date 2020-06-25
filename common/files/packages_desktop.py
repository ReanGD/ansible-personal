# global x86_64, hostname_id, distro, network_type, virtualization, develop

pkgs = []
grps = []

is_notebook = hostname_id in ["archnote"]


def system_pkgs():
    if x86_64:
        return ["yay"] # AUR package manager
    else:
        return []

def network_pkgs():
    return ["netctl",  # arch specific network manager
            "openssh"]  # ssh server

def virtualization_pkgs():
    if virtualization == "kvm_qemu":
        return ["qemu",
                "virt-viewer",  # for SPICE
                "edk2-ovmf"]  # for UEFI
    elif virtualization == "kvm_libvirt":
        return ["qemu",
                "libvirt",  # additional interface
                "virt-viewer",  # for SPICE
                "virt-manager",  # GUI for libvirt
                "edk2-ovmf",  # for UEFI
                "ebtables",  # for network
                "dnsmasq",  # for network
                "python-lxml"]  # for ansible
    else:
        return []

def develop_pkgs():
    if develop == "none":
        return []

    develop_pkgs = []
    develops = develop.split(",")
    if "utils" in develops:
        # "pycharm-community-edition", "pycharm-professional", "clion", "clion-cmake"
        develop_pkgs += ["git",
                         "icdiff",  # console diff
                         "meld",
                         "emacs",
                         "sublime-text-dev",
                         "visual-studio-code-bin"]

    if "cpp" in develops:
        develop_pkgs += ["clang",
                         "cmake",
                         "ninja",
                         "gdb",
                         "cpp-dependencies",
                         "python-dateutil", # for include-what-you-use
                         "include-what-you-use"]

    if "python" in develops:
        develop_pkgs += ["python",
                         "python-pip",
                         "python-nose",
                         "python-jedi",
                         "python-pylint",
                         "flake8",
                         "python-pytest",
                         "python-termcolor",
                         "python-virtualenv",
                         "tk",
                         "swig",
                         "portaudio"]  # for pyaudio and my audio-lib

    if "go" in develops:
        develop_pkgs += ["go"]

    if "rust" in develops:
        develop_pkgs += ["rust", "cargo", "rust-src", "rust-racer"]

    if "rust3D" in develops:
        develop_pkgs += ["sdl2", "sdl2_image"]

    if "protobuf" in develops:
        develop_pkgs += ["protobuf"]

    if "sqlite" in develops:
        develop_pkgs += ["sqlite-analyzer"]

    if "android" in develops:
        develop_pkgs += ["adb"]

    return develop_pkgs

# drivers
pkgs += ["mesa"]

if hostname_id == "archhost":
    pkgs += ["nvidia",
             "lib32-nvidia-utils"  # for steam
             ]
elif hostname_id == "archnote":
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

if hostname_id == "archhost":
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
         "noto-fonts-emoji",  # emoji for chrome
         "adobe-source-code-pro-fonts"]

# terminal
pkgs += ["urxvt-perls",
         "zsh",
         "libnewt",  # external dialog
         "oh-my-zsh-git",
         "zsh-syntax-highlighting",
         "fzf"]

# system
pkgs += ["refind",
         "polkit",
         "gnupg",
         "xcursor-ize-vision",  # a couple of X cursor that similar to Windows 7 cursor.
         "pkgfile",  # pkgfile makepkg (get package for makepkg)
         "pkgcacheclean",  # clean the pacman cache
         "perwindowlayoutd",  # daemon to make per window layout (also exists "kbdd-git")
         "libnotify",  # create notifications message
         "bind-tools",  # dig and etc
         "ansible",
         "rsync",
         "git",
         "nano",
         "vim"]

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
         # "tor-browser-ru",
         "google-chrome",
         ]

# file managers
pkgs += ["doublecmd-gtk2",
         "fsearch-git",
         "transmission-remote-gui",  # transmission-remote-gui-bin - not work now
         "yandex-disk",  # yandex-disk setup/start
         "dropbox"]

if not is_notebook:
    pkgs += ["transmission-remote-gui"]

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
pkgs += ["mupdf",  # pdf viewer (analog: llpp-git)
         "libreoffice-fresh-ru"
         ]

# spell checkers
pkgs += ["enchant", "hunspell-en_US", "hunspell-ru-aot", "languagetool"]

# xorg
pkgs += ["xorg-xfontsel",  # font select
         "xorg-xprop",  # window info (xprop | grep WM_CLASS)
         "xorg-xev",  # keypress info
         "xorg-xwininfo",  # select window
         "xrectsel"]  # get select region

if is_notebook:
    pkgs += ["xorg-xbacklight"]  # backlight control application (xbacklight -set 40)

# Containerization
pkgs += ["docker", "docker-compose"]

pkgs += system_pkgs()
pkgs += network_pkgs()
pkgs += virtualization_pkgs()
pkgs += develop_pkgs()

# game
pkgs += ["playonlinux",
        "steam",
        "lib32-libldap",  # for WOT ?
        "minecraft"]

# messengers
pkgs += ["telegram-desktop", "slack-desktop"]

# groups
grps += ["base-devel"]

packages = pkgs
groups = grps
