# global x86_64, hostname_id, distro, network_type, virtualization, gui, develop, monitoring, roles


# pylama:ignore=E0602
def is_manjaro() -> bool:
    return distro == "manjaro"  # type: ignore


def is_x86_64() -> bool:
    return x86_64  # type: ignore


def is_role(name: str) -> bool:
    return name in roles.split(",")  # type: ignore


def is_monitoring(name: str) -> bool:
    return name in monitoring.split(",")  # type: ignore


def is_gui(name: str) -> bool:
    return name in gui.split(",")  # type: ignore


def is_develop(name: str) -> bool:
    return name in develop.split(",")  # type: ignore


def is_network_type(name: str) -> bool:
    return name in network_type.split(",")  # type: ignore


def get_hostname_id() -> bool:
    return hostname_id  # type: ignore


def get_virtualization() -> bool:
    return virtualization  # type: ignore


def system():
    system_pkgs = []
    if is_manjaro():
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

    if is_x86_64():
        system_pkgs += ["yay",  # AUR package manager
                        "refind",  # UEFI boot manager
                        "pkgcacheclean"]  # clean the pacman cache

    return system_pkgs


def driver():
    driver_pkgs = []

    if not is_gui("none"):
        driver_pkgs = ["mesa"]

    if get_hostname_id() == "archhost":
        driver_pkgs += ["nvidia"]
    elif get_hostname_id() == "xnote":
        driver_pkgs += ["bbswitch",
                        # "bumblebee",
                        # "nvidia",
                        "xf86-video-intel",
                        "xf86-input-libinput"]  # touchpad
    elif get_hostname_id() == "worknote":
        driver_pkgs += ["bbswitch",
                        # "bumblebee",
                        # "nvidia",
                        "xf86-video-intel",
                        "xf86-input-libinput"]  # touchpad
    elif get_hostname_id() == "kvmtest":
        driver_pkgs += ["spice-vdagent", "xf86-video-qxl"]

    return driver_pkgs


def network():
    network_pkgs = ["net-tools",
                    "smbclient",
                    "httpie",
                    "openvpn",
                    "openssh"]  # ssh server

    if is_network_type("wireless"):
        network_pkgs += ["iwd"]

    return network_pkgs


def vm():
    if get_virtualization() == "kvm_qemu":
        return ["qemu",
                "virt-viewer",  # for SPICE
                "edk2-ovmf"]  # for UEFI
    elif get_virtualization() == "kvm_libvirt":
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
    if is_gui("none"):
        return []

    gui_pkgs = ["xorg-server",
                "xorg-xinit",
                "xorg-xfontsel",  # font select
                "xorg-xprop",  # window info (xprop | grep WM_CLASS)
                "xorg-xev",  # keypress info
                "xorg-xwininfo",  # select window
                "arandr",  # screen position
                "ddcutil",  # brightness\monitor control
                "redshift",  # brightness control
                "xcursor-ize-vision",  # a couple of X cursor that similar to Windows 7 cursor
                "perwindowlayoutd",  # daemon to make per window layout (also exists "kbdd-git")
                "scrot",  # for screenshots
                "flameshot",  # for screenshots
                "libnotify",  # create notifications message
                "wmctrl",  # windows manipulation
                "xclip",  # save data to clipboard
                "xrectsel"]  # get select region

    # rofi
    gui_pkgs += ["rofi", "rofi-proxy", "python-googletrans", "python-psutil"]

    if is_gui("lightdm"):
        gui_pkgs += ["lightdm", "lightdm-gtk-greeter"]

    if is_gui("awesome"):
        gui_pkgs += ["awesome",
                     "mate-icon-theme",
                     "inter-font"]

    if is_gui("cinnamon"):
        gui_pkgs += ["cinnamon"]

    if is_gui("kde"):
        gui_pkgs += ["plasma-desktop", "kdeconnect", "dolphin-plugins", "print-manager"]
        if is_manjaro():
            gui_pkgs += ["manjaro-kde-settings",
                         "manjaro-settings-manager-knotifier",
                         "manjaro-settings-manager-kcm",
                         "pamac-gtk"]

    return gui_pkgs


def development():
    if is_develop("none"):
        return []

    develop_pkgs = []
    if is_develop("std"):
        # "pycharm-community-edition", "pycharm-professional", "clion", "clion-cmake"
        develop_pkgs += ["git",
                         "icdiff",  # console diff
                         "meld",
                         "emacs",
                         "sublime-merge",
                         "sublime-text-dev",
                         "visual-studio-code-bin"]

    if is_develop("cpp"):
        develop_pkgs += ["clang",
                         "cmake",
                         "ninja",
                         "gdb",
                         "protobuf",
                         "cpupower",  # for disable CPU powersafe mode in tests
                         "cpp-dependencies",
                         "python-dateutil",  # for include-what-you-use
                         "include-what-you-use"]

    if is_develop("python"):
        develop_pkgs += ["python-pip",
                         "python-nose",
                         "python-jedi",  # for vs-code ?
                         "pylama",  # linter
                         "mypy",  # linter
                         "python-pylint",  # linter
                         "python-pytest",
                         "python-termcolor",  # for ansible
                         "python-virtualenv",
                         "tk",
                         "swig",
                         "portaudio"]  # for pyaudio and my audio-lib

    if is_develop("go"):
        develop_pkgs += ["go", "protobuf"]

    if is_develop("rust"):
        develop_pkgs += ["rust", "cargo", "rust-src", "rust-racer"]

    if is_develop("rust3D"):
        develop_pkgs += ["sdl2", "sdl2_image"]

    if is_develop("sqlite"):
        develop_pkgs += ["sqlite-analyzer"]

    if is_develop("android"):
        develop_pkgs += ["adb"]

    return develop_pkgs


def monitoring_utils():
    if is_monitoring("none"):
        return []

    monitoring_pkgs = []
    if is_monitoring("std"):
        monitoring_pkgs += ["iftop",  # network monitor
                            "htop",  # process monitor
                            "iotop",  # disk monitor
                            "hwinfo"]  # info about hardware

        if is_x86_64():
            monitoring_pkgs += ["hw-probe"]  # check hardware and find drivers

    if is_monitoring("notebook"):
        monitoring_pkgs += ["powertop"]

    if is_monitoring("hddtemp"):
        monitoring_pkgs += ["hddtemp",  # disk temperature
                            "smartmontools"]

    if is_monitoring("ups"):
        monitoring_pkgs += ["apcupsd"]

    return monitoring_pkgs


def font():
    if not is_role("font"):
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
    if not is_role("docker"):
        return []

    return ["docker", "docker-compose"]


def automount():
    if not is_role("automount"):
        return []

    return ["nfs-utils"]


def web():
    if not is_role("web"):
        return []

    return ["firefox", "firefox-i18n-ru", "google-chrome"]


def game():
    if not is_role("game"):
        return []

    game_pkgs = []
    if is_manjaro():
        game_pkgs += ["steam-manjaro"]
    else:
        game_pkgs += ["steam"]

    game_pkgs += ["playonlinux",
                  "lib32-libldap",  # for WOT ?
                  "minecraft"]

    return game_pkgs


def messengers():
    if not is_role("messengers"):
        return []

    return ["telegram-desktop", "slack-desktop"]


def audio():
    if not is_role("audio"):
        return []

    audio_pkgs = ["pulseaudio"]

    if not is_gui("none"):
        audio_pkgs += ["pavucontrol", "volumeicon", "pasystray"]

    return audio_pkgs


def media():
    if not is_role("media"):
        return []

    return ["viewnior",  # image viewer
            "gimp",
            "blender",
            "smplayer",
            "deadbeef"]


def pdf():
    if not is_role("pdf"):
        return []

    return ["mupdf"]  # pdf viewer (analog: llpp-git)


def office():
    if not is_role("office"):
        return []

    return ["libreoffice-fresh-ru"]


def file_managers():
    if not is_role("file_managers"):
        return []

    return ["doublecmd-gtk2",
            "fsearch-git",
            "yandex-disk",  # yandex-disk setup/start
            "dropbox"]


def torrent():
    if not is_role("torrent"):
        return []

    return ["transmission-remote-gui"]  # transmission-remote-gui-bin - not work now


def spell_checkers():
    if not is_role("spell_checkers"):
        return []

    return ["enchant", "hunspell-en_US", "hunspell-ru-aot", "languagetool"]


def plex():
    if not is_role("plex"):
        return []

    return ["plex-media-server"]


def work():
    if not is_role("work"):
        return []

    return ["openconnect"]  # for vpn to work


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
