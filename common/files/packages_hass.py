# global host
pkgs = []
grps = []

# system
pkgs += ["raspberrypi-firmware", "raspberrypi-bootloader-x", "linux-raspberrypi", "raspberrypi-bootloader"]

# monitoring
pkgs += ["rsync",
         "gnupg",
         "iftop",  # network monitor
         "htop",  # process monitor
         "iotop",  # disk monitor
         "hddtemp",  # disk temperature
         "smartmontools"]

# net tools
pkgs += ["net-tools", "openssh"]

# python
pkgs += ["python", "python-pip", "python-virtualenv"]

# build tools
pkgs += ["libffi", "libudev0-shim"]

# hass deps
pkgs += ["protobuf", "mosquitto"]

# groups
grps += ["base", "base-devel"]

packages = pkgs
groups = grps
