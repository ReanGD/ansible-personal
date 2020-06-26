# global x86_64, hostname_id, distro, network_type, virtualization, gui, develop, monitoring, roles

pkgs = []
grps = []

is_notebook = hostname_id in ["archnote"]


def system_pkgs():
    system_pkgs = ["base",
                   "polkit",
                   "wget",
                   "curl",
                   "git",
                   "rsync",
                   "logrotate",
                   "nano",
                   "vim",
                   "pacutils",
                   "pkgfile",  # pkgfile makepkg (get package for makepkg)
                   "mlocate",
                   "man-db"]
    if x86_64:
        system_pkgs += ["yay",  # AUR package manager
                        "refind",  # UEFI boot manager
                        "pkgcacheclean"]  # clean the pacman cache

    return system_pkgs

def driver_pkgs():
    driver_pkgs = ["mesa"]

    if hostname_id == "archhost":
        driver_pkgs += ["nvidia"]
    elif hostname_id == "archnote":
        driver_pkgs += ["bbswitch",
                        # "bumblebee",
                        # "nvidia",
                        "xf86-video-intel",
                        "xf86-input-libinput"]  # touchpad

    return driver_pkgs

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

def gui_pkgs():
    if gui == "none":
        return []

    gui_pkgs = ["xorg-server",
                "xorg-xinit",
                "xorg-xfontsel",  # font select
                "xorg-xprop",  # window info (xprop | grep WM_CLASS)
                "xorg-xev",  # keypress info
                "xorg-xwininfo",  # select window
                "xrectsel"]  # get select region

    guis = gui.split(",")
    if "lightdm" in guis:
        gui_pkgs += ["lightdm", "lightdm-gtk-greeter"]

    if "awesome" in guis:
        gui_pkgs += ["awesome", "vicious"]

    if "cinnamon" in guis:
        gui_pkgs += ["cinnamon"]

    if "notebook" in guis:
        gui_pkgs += ["xorg-xbacklight"]  # backlight control application (xbacklight -set 40)

    return gui_pkgs

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

def monitoring_pkgs():
    if monitoring == "none":
        return []

    monitoring_pkgs = []
    if "std" in monitoring.split(","):
        monitoring_pkgs += ["iftop",  # network monitor
                            "htop",  # process monitor
                            "iotop",  # disk monitor
                            "hwinfo"]  # info about hardware

        if x86_64:
            monitoring_pkgs+=["hw-probe"]  # check hardware and find drivers

    if "notebook" in monitoring.split(","):
        monitoring_pkgs+=["powertop"]

    if "hddtemp" in monitoring.split(","):
        monitoring_pkgs+=["hddtemp",  # disk temperature
                          "smartmontools"]

    if "ups" in monitoring.split(","):
        monitoring_pkgs+=["apcupsd"]

    return monitoring_pkgs

def font_pkgs():
    if "font" not in roles.split(","):
        return []
    return ["font-manager",  # viewer for fonts
            "ttf-ms-fonts",
            "ttf-tahoma",
            # "ttf-vista-fonts",
            "ttf-fixedsys-excelsior-linux",
            "ttf-droid",
            "ttf-dejavu",
            "ttf-ubuntu-font-family",
            "noto-fonts-emoji",  # emoji for chrome
            "adobe-source-code-pro-fonts"]

def docker_pkgs():
    if "docker" not in roles.split(","):
        return []
    return ["docker", "docker-compose"]

def automount_pkgs():
    if "automount" not in roles.split(","):
        return []
    return ["nfs-utils"]


# terminal
pkgs += ["urxvt-perls",
         "zsh",
         "libnewt",  # external dialog
         "oh-my-zsh-git",
         "zsh-syntax-highlighting",
         "fzf"]

# system
pkgs += ["gnupg",
         "xcursor-ize-vision",  # a couple of X cursor that similar to Windows 7 cursor.
         "perwindowlayoutd",  # daemon to make per window layout (also exists "kbdd-git")
         "libnotify",  # create notifications message
         "bind-tools",  # dig and etc
         "ansible"]

# WM
pkgs += ["rofi"]  # run app menu

# net tools
pkgs += ["net-tools",
         "dialog",
         "smbclient",
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

pkgs += system_pkgs()
pkgs += driver_pkgs()
pkgs += network_pkgs()
pkgs += virtualization_pkgs()
pkgs += gui_pkgs()
pkgs += develop_pkgs()
pkgs += monitoring_pkgs()
pkgs += font_pkgs()
pkgs += docker_pkgs()
pkgs += automount_pkgs()

# game
pkgs += ["playonlinux",
        "steam",
        "lib32-nvidia-utils",  # for steam
        "lib32-libldap",  # for WOT ?
        "minecraft"]

# messengers
pkgs += ["telegram-desktop", "slack-desktop"]

# groups
grps += ["base-devel"]

packages = pkgs
groups = grps
