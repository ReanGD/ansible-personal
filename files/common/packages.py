# global x86_64, hostname_id, distro, network_type, dmanager, gui, develop, monitoring, roles


# pylama:ignore=E0602
def is_x86_64() -> bool:
    return x86_64  # type: ignore


def is_role(name: str) -> bool:
    return name in roles.split(",")  # type: ignore


def is_monitoring(name: str) -> bool:
    return name in monitoring.split(",")  # type: ignore


def is_dmanager(name: str) -> bool:
    return name in dmanager.split(",")  # type: ignore


def is_gui(name: str) -> bool:
    return name in gui.split(",")  # type: ignore


def is_develop(name: str) -> bool:
    return name in develop.split(",")  # type: ignore


def is_network_type(name: str) -> bool:
    return name in network_type.split(",")  # type: ignore

def is_work_host() -> bool:
    return hostname_id == "worknote"  # type: ignore

def get_hostname_id() -> str:
    return hostname_id  # type: ignore


def system():
    system_pkgs = ["gnupg",
                   "base",
                   "inetutils",  # for set hostname (crazy ansible code)
                   "rsync",
                   "dialog",
                   "nano",
                   "bat"]

    if not is_x86_64():
        return system_pkgs

    # utils
    system_pkgs += ["linux",
                    "linux-firmware",
                    "polkit",
                    "wget",
                    "curl",
                    "git",
                    "jq",
                    "logrotate",
                    "vim",
                    "pacutils",
                    "pkgfile",  # pkgfile makepkg (get package for makepkg)
                    "libnewt",  # external dialog
                    "man-db"]

    # ansible
    system_pkgs += ["ansible", "python", "python-lxml"]

    # terminal
    system_pkgs += ["fd",       # fast find alternative
                    "ripgrep",  # fast grep
                    "exa",      # ls alternative
                    "ncdu",     # disk usage analyzer
                    "zsh",
                    "fzf"]

    if not is_gui("none"):
        system_pkgs += ["terminator",
                        "bitwarden-cli"]
    else:
        system_pkgs += ["rxvt-unicode-terminfo"]

    # archivers
    system_pkgs += ["p7zip", "unzip", "unrar"]

    if is_x86_64():
        system_pkgs += ["yay",  # AUR package manager
                        "refind",  # UEFI boot manager
                        "debtap",  # install deb packages
                        "pkgcacheclean",  # clean the pacman cache
                        ]

    return system_pkgs


def driver():
    driver_pkgs = []

    if not is_x86_64():
        return driver_pkgs

    if not is_gui("none"):
        driver_pkgs = ["mesa"]

    if get_hostname_id() == "server":
        #  "xf86-video-intel"
        driver_pkgs += ["btrfs-progs"]
    elif get_hostname_id() == "master":
        driver_pkgs += ["nvidia",
                        "gwe"]  # Controlling NVIDIA Fans
    elif get_hostname_id() == "xnote":
        driver_pkgs += ["bbswitch",
                        # "bumblebee",
                        # "nvidia",
                        "xf86-video-intel",
                        "xf86-input-libinput"]  # touchpad
    elif get_hostname_id() == "worknote":
        driver_pkgs += ["sof-firmware",  # sound
                        "vulkan-intel",
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

    if is_network_type("networkmanager"):
        network_pkgs += ["networkmanager"]

    return network_pkgs


def desktop_env():
    if is_gui("none"):
        return []

    gui_pkgs = ["xorg-server",
                "xorg-xinit",
                "xorg-xfontsel",  # font select
                "xorg-xprop",  # window info (xprop | grep WM_CLASS)
                "xorg-xev",  # keypress info
                "xorg-xwininfo",  # select window
                "xsel",  # get clipboard data
                "arandr",  # screen position
                "ddcutil",  # brightness\monitor control
                "xcursor-ize-vision",  # a couple of X cursor that similar to Windows 7 cursor
                "perwindowlayoutd",  # daemon to make per window layout (also exists "kbdd-git")
                "scrot",  # for screenshots
                "flameshot",  # for screenshots
                "libnotify",  # create notifications message
                "wmctrl",  # windows manipulation
                "xclip",  # save data to clipboard
                "gsmartcontrol",  # UI for smartctl
                "desktop-file-utils",  # for apply desktop files
                "xrectsel"]  # get select region

    # rofi
    # "python-googletrans",
    # "rofi-proxy"
    gui_pkgs += ["rofi", "python-psutil"]

    if is_dmanager("lightdm"):
        gui_pkgs += ["lightdm", "lightdm-gtk-greeter"]

    if is_dmanager("sddm"):
        gui_pkgs += ["sddm"]

    if is_gui("qtile"):
        gui_pkgs += ["qtile"]

    if is_gui("hyprland"):
        gui_pkgs += ["hyprland", "hyprlock", "waybar"]

    if is_gui("awesome"):
        gui_pkgs += ["awesome",
                     "mate-icon-theme",
                     "inter-font"]

    if is_gui("qtile") or is_gui("awesome"):
        gui_pkgs += ["redshift",  # brightness control
                     "polybar",
                     ]

    if is_gui("kde"):
        gui_pkgs += ["kdeconnect",  # connect to phone
                     "plasma5-applets-virtual-desktop-bar-git",  # tilling bar
                     "dolphin-plugins",
                     "print-manager"]

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
                         "ansible-lint",  # for ansible plugin in vscode
                         "visual-studio-code-bin"]

    if is_develop("cpp"):
        develop_pkgs += ["clang",
                         "cmake",
                         "ninja",
                         "gdb",
                         "conan",
                         "protobuf",
                         "cpupower",  # for disable CPU powersafe mode in tests
                         # "python-dateutil",  # for include-what-you-use
                         # "include-what-you-use",
                         # "vulkan-mesa-layers",  # show vulkan draw statistics
                        #  "cpp-dependencies",  # show dependencies graph
                         ]

    if is_develop("python"):
        develop_pkgs += ["python-pip",
                         "python-nose",
                         "python-jedi",  # for vs-code ?
                         "pyenv",  # install others versions of python
                         "python-poetry",  # project deps manager
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
        develop_pkgs += ["android-tools",  # for adb
                         "jdk8-openjdk",  # for flutter
                         "android-sdk",  # for flutter
                         "android-sdk-platform-tools",  # for flutter
                         "android-sdk-build-tools",  # for flutter
                         "flutter"]

    return develop_pkgs


def monitoring_utils():
    if is_monitoring("none"):
        return []

    monitoring_pkgs = []
    if is_monitoring("std"):
        monitoring_pkgs += ["iftop",  # network monitor
                            "htop",  # process monitor
                            "iotop"]  # disk monitor

        if is_x86_64():
            monitoring_pkgs += ["hwinfo",    # info about hardware
                                ]
                                # "hw-probe"  # check hardware and find drivers, need fix dependencies

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


def k8s():
    if not is_role("k8s"):
        return []

    return ["helm"]


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

    game_pkgs = ["steam"]

    # game_pkgs += ["minecraft-launcher"]

    return game_pkgs


def messengers():
    if not is_role("messengers"):
        return []

    messengers_pkgs = ["telegram-desktop"]

    if is_work_host():
        messengers_pkgs += ["zoom"]

    return messengers_pkgs


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
            "krita",
            "inkscape",  # vector editor
            "blender",
            "smplayer",
            "deadbeef"]


def office():
    if not is_role("office"):
        return []

    return ["libreoffice-fresh-ru",
            "obsidian",
            "mupdf",  # pdf viewer (analog: llpp-git)
            "enchant", "hunspell-en_us", "hunspell-ru-aot", "languagetool",  # spell checkers
            ]


def file_managers():
    if not is_role("file_managers"):
        return []

    return ["doublecmd-gtk2",
            "fsearch-git",
            "yandex-disk",  # yandex-disk setup/start
            "dropbox"]


def file_managers_keys():
    if not is_role("file_managers"):
        return []

    # dropbox
    return ["1C61A2656FB57B7E4DE0F4C1FC918B335044912E"]


def torrent():
    if not is_role("torrent"):
        return []

    return ["transmission-remote-gui"]  # transmission-remote-gui-bin - not work now


def bluetooth():
    if not is_role("bluetooth"):
        return []

    if not is_gui("kde"):
        return ["bluez-qt"]

    return []


def rsync_server():
    if not is_role("rsync_server"):
        return []

    return ["rsync"]


def hass():
    if not is_role("hass"):
        return []

    hass_pkgs = []

    # raspberry
    hass_pkgs += ["raspberrypi-firmware", "raspberrypi-bootloader-x", "raspberrypi-bootloader", "linux-rpi"]

    # hass deps
    hass_pkgs += ["protobuf", "libjpeg-turbo", "rust", "unzip"]

    # build tools
    hass_pkgs += ["gcc", "make", "pkgconf", "libffi", "libudev0-shim"]

    # python
    hass_pkgs += ["python", "python-pip", "python-virtualenv"]

    # tls
    hass_pkgs += ["certbot"]

    return hass_pkgs


def work():
    if not is_role("work"):
        return []

    return ["openconnect",  # for vpn to work
            "allure-commandline",  # view allure report
            "bazelisk",  # build tool for bazel
            ]


def sing_box():
    if not is_role("sing_box"):
        return []

    return ["sing-box"]


metas = ["base-devel"]
groups = []

packages = []
packages += system()
packages += driver()
packages += network()
packages += desktop_env()
packages += development()
packages += monitoring_utils()
packages += font()
packages += docker()
packages += k8s()
packages += automount()
packages += web()
packages += game()
packages += messengers()
packages += audio()
packages += media()
packages += office()
packages += file_managers()
packages += torrent()
packages += bluetooth()
packages += rsync_server()
packages += hass()
packages += work()
packages += sing_box()

ignore_packages = ["squadus"]

keys = []
keys += file_managers_keys()
