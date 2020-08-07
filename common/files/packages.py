# global x86_64, hostname_id, distro, network_type, virtualization, gui, develop, monitoring, roles

def system():
    system_pkgs = []
    if distro == "manjaro":
        system_pkgs += ["linux-lts"]
    else:
        system_pkgs += ["linux"]

    # utils
    system_pkgs += ["linux-firmware",
                    "base",
                    "polkit",
                    "gnupg",
                    "wget",
                    "curl",
                    "git",
                    "rsync",
                    "logrotate",
                    "nano",
                    "vim",
                    "pacutils",
                    "pkgfile",  # pkgfile makepkg (get package for makepkg)
                    "dialog",
                    "libnewt",  # external dialog
                    "mlocate",
                    "man-db"]

    # ansible
    system_pkgs += ["ansible", "python", "python-lxml"]

    # terminal
    system_pkgs += ["urxvt-perls",
                    "fd",  # fast find alternative
                    "exa",  # ls alternative
                    "zsh",
                    "fzf"]

    # archivers
    system_pkgs += ["p7zip", "unzip", "unrar"]

    if x86_64:
        system_pkgs += ["yay",  # AUR package manager
                        "refind",  # UEFI boot manager
                        "pkgcacheclean"]  # clean the pacman cache

    return system_pkgs

def driver():
    driver_pkgs = []

    if gui != "none":
        driver_pkgs = ["mesa"]

    if hostname_id == "archhost":
        driver_pkgs += ["nvidia"]
    elif hostname_id == "xnote":
        driver_pkgs += ["bbswitch",
                        # "bumblebee",
                        # "nvidia",
                        "xf86-video-intel",
                        "xf86-input-libinput"]  # touchpad
    elif hostname_id == "kvmtest":
        driver_pkgs += ["spice-vdagent", "xf86-video-qxl"]

    return driver_pkgs

def network():
    network_pkgs = ["net-tools",
                    "smbclient",
                    "httpie",
                    "openvpn",
                    "openssh"]  # ssh server

    if "wireless" in network_type.split(","):
        network_pkgs += ["iwd"]

    return network_pkgs

def vm():
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
                "dnsmasq"]  # for network
    else:
        return []

def desktop_env():
    if gui == "none":
        return []

    gui_pkgs = ["xorg-server",
                "xorg-xinit",
                "xorg-xfontsel",  # font select
                "xorg-xprop",  # window info (xprop | grep WM_CLASS)
                "xorg-xev",  # keypress info
                "xorg-xwininfo",  # select window
                "arandr",  # screen position
                "xcursor-ize-vision",  # a couple of X cursor that similar to Windows 7 cursor
                "perwindowlayoutd",  # daemon to make per window layout (also exists "kbdd-git")
                "scrot",  # for screenshots
                "flameshot",  # for screenshots
                "libnotify",  # create notifications message
                "wmctrl",  # windows manipulation
                "xclip",  # save data to clipboard
                "xrectsel"]  # get select region

    guis = gui.split(",")
    if "lightdm" in guis:
        gui_pkgs += ["lightdm", "lightdm-gtk-greeter"]

    if "awesome" in guis:
        gui_pkgs += ["awesome",
                     "mate-icon-theme",
                     "inter-font",
                     "rofi"]  # run app menu

    if "cinnamon" in guis:
        gui_pkgs += ["cinnamon"]

    if "kde" in guis:
        gui_pkgs += ["plasma-desktop", "kdeconnect", "dolphin-plugins", "print-manager"]
        if distro == "manjaro":
            gui_pkgs += ["manjaro-kde-settings", "manjaro-settings-manager-knotifier", "manjaro-settings-manager-kcm", "pamac-gtk"]

    if "notebook" in guis:
        gui_pkgs += ["xorg-xbacklight"]  # backlight control application (xbacklight -set 40)

    return gui_pkgs

def development():
    if develop == "none":
        return []

    develop_pkgs = []
    develops = develop.split(",")
    if "std" in develops:
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
                         "protobuf",
                         "cpp-dependencies",
                         "python-dateutil", # for include-what-you-use
                         "include-what-you-use"]

    if "python" in develops:
        develop_pkgs += ["python-pip",
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
        develop_pkgs += ["go", "protobuf"]

    if "rust" in develops:
        develop_pkgs += ["rust", "cargo", "rust-src", "rust-racer"]

    if "rust3D" in develops:
        develop_pkgs += ["sdl2", "sdl2_image"]

    if "sqlite" in develops:
        develop_pkgs += ["sqlite-analyzer"]

    if "android" in develops:
        develop_pkgs += ["adb"]

    return develop_pkgs

def monitoring_utils():
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

def font():
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
            "inter-font",  # for awesome
            "noto-fonts-emoji",  # emoji for chrome
            "adobe-source-code-pro-fonts"]

def docker():
    if "docker" not in roles.split(","):
        return []
    return ["docker", "docker-compose"]

def automount():
    if "automount" not in roles.split(","):
        return []
    return ["nfs-utils"]

def web():
    if "web" not in roles.split(","):
        return []
    return ["firefox", "firefox-i18n-ru", "google-chrome"]

def game():
    if "game" not in roles.split(","):
        return []
    return ["playonlinux",
            "steam",
            "lib32-nvidia-utils",  # for steam
            "lib32-libldap",  # for WOT ?
            "minecraft"]

def messengers():
    if "game" not in roles.split(","):
        return []
    return ["telegram-desktop", "slack-desktop"]

def audio():
    if "audio" not in roles.split(","):
        return []

    audio_pkgs = ["pulseaudio"]

    if gui != "none":
        audio_pkgs += ["pavucontrol", "volumeicon", "pasystray"]

    return audio_pkgs

def media():
    if "media" not in roles.split(","):
        return []

    return ["viewnior",  # image viewer
            "gimp",
            "blender",
            "smplayer",
            "deadbeef"]

def pdf():
    if "pdf" not in roles.split(","):
        return []

    return ["mupdf"]  # pdf viewer (analog: llpp-git)

def office():
    if "office" not in roles.split(","):
        return []

    return ["libreoffice-fresh-ru"]

def file_managers():
    if "file_managers" not in roles.split(","):
        return []

    return ["doublecmd-gtk2",
            "fsearch-git",
            "yandex-disk",  # yandex-disk setup/start
            "dropbox"]

def torrent():
    if "torrent" not in roles.split(","):
        return []

    return ["transmission-remote-gui"]  # transmission-remote-gui-bin - not work now

def spell_checkers():
    if "spell_checkers" not in roles.split(","):
        return []

    return ["enchant", "hunspell-en_US", "hunspell-ru-aot", "languagetool"]

def plex():
    if "plex" not in roles.split(","):
        return []

    return ["plex-media-server"]

def work():
    if "work" not in roles.split(","):
        return []

    return ["openconnect"] # for vpn to work

grps = ["base-devel"]

pkgs = []
pkgs += system()
pkgs += driver()
pkgs += network()
pkgs += vm()
pkgs += desktop_env()
pkgs += development()
pkgs += monitoring_utils()
pkgs += font()
pkgs += docker()
pkgs += automount()
pkgs += web()
pkgs += game()
pkgs += messengers()
pkgs += audio()
pkgs += media()
pkgs += pdf()
pkgs += office()
pkgs += spell_checkers()
pkgs += file_managers()
pkgs += torrent()
pkgs += plex()
pkgs += work()

packages = pkgs
groups = grps
