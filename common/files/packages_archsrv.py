# global host
pkgs = []
grps = []

# monitoring
pkgs += ["iftop",  # network monitor
         "htop",  # process monitor
         "iotop",  # disk monitor
         "hddtemp",  # disk temperature
         "smartmontools"]

# system
pkgs += ["refind-efi",
         "gnupg",
         "pkgfile",  # pkgfile makepkg (get package for makepkg)
         "pkgcacheclean",  # clean the pacman cache         
         "yay",  # AUR package manager
         "ansible",
         "rsync"]

# net tools
pkgs += ["wget", "nfs-utils", "openssh"]

# python
pkgs += ["python"]

# git
pkgs += ["git"]

# VM
pkgs += ["docker", "docker-compose"]

# media
pkgs += ["plex-media-server"]

# groups
grps += ["base", "base-devel"]

packages = pkgs
groups = grps
