#!/usr/bin/env python
import os
import subprocess


def parse_cmd(cmd):
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = p.communicate()
    return set(out.decode("UTF-8").split())


def all_packages():
    return parse_cmd(["pacman", "-Qq"])


def explicit_packages():
    return parse_cmd(["pacman", "-Qeq"])


def all_depends(package):
    l = parse_cmd(["pactree", "-u", package])
    l.discard(package)
    return l


def load_config(config_path):
    if not os.path.isfile(config_path):
        config_path = os.path.join(os.getcwd(), config_path)
    config_data = {}
    exec(open(config_path).read(), config_data)
    return set(config_data["pkgs"])

config_pkgs = load_config("config.py")
explicit_pkgs = explicit_packages()
print(len(explicit_pkgs))
new_pkgs = explicit_pkgs.difference(config_pkgs)
print(len(new_pkgs))
print(new_pkgs)
