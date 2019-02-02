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
         "aurman",  # AUR package manager
         "rsync"]

# net tools
pkgs += ["wget", "nfs-utils"]

# python
pkgs += ["python"]

# git
pkgs += ["git"]

# VM
pkgs += ["docker", "docker-compose"]

packages = pkgs
groups = grps
ignore_packages = ["yaourt", "ansible"]
ignore_groups = ["base", "base-devel"]
