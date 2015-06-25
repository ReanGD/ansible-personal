pkgs = []

# font packages
pkgs += ["freetype2-ubuntu",
         "fontconfig-ubuntu",
         "cairo-ubuntu",
         "ttf-ms-fonts",
         "ttf-fixedsys-excelsior-linux",
         "ttf-droid",
         "ttf-dejavu",
         "ttf-ubuntu-font-family",
         "adobe-source-code-pro-fonts"]

# terminal
pkgs += ["rxvt-unicode-patched", "urxvt-perls-git", "zsh", "oh-my-zsh-git"]

# web
pkgs += ["firefox", "firefox-i18n-ru", "flashplugin"]

# cpp
pkgs += ["boost", "clang", "gtest", "zeromq", "valgrind", "cmake"]

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
         "python2-pylint",
         "flake8",
         "python2-flake8"]

# text editors
pkgs += ["emacs", "vim", "sublime-text-nightly"]

# git
pkgs += ["git", "meld"]

# archive program
pkgs += ["p7zip", "unzip", "unrar"]

# android
pkgs += ["adb"]

# xorg
pkgs += ["xorg-xfontsel",  # font select
         "xorg-xprop",     # window info (xprop | grep WM_CLASS)
         "xorg-xev"]       # keypress info


packages = pkgs
ignore_packages = ["yaourt", "package-query"]
ignore_groups = ["base", "base-devel"]
