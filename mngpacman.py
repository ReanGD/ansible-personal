#!/usr/bin/env python
import os
import platform
import subprocess


class PackageManager(object):
    def all_packages(self):
        raise NotImplementedError()

    def explicit_packages(self):
        raise NotImplementedError()

    def depend_packages(self, package):
        raise NotImplementedError()

    def group_depend_packages(self, group):
        raise NotImplementedError()


class PacmanManager(PackageManager):
    def __parse(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()
        return set(out.decode("UTF-8").split())

    def all_packages(self):
        return self.__parse(["pacman", "-Qq"])

    def explicit_packages(self):
        return self.__parse(["pacman", "-Qeq"])

    def depend_packages(self, package):
        l = self.__parse(["pactree", "-u", package])
        l.discard(package)
        return l

    def groups_depend_packages(self, groups):
        pkgs = set()
        for it in groups:
            pkgs.update(self.__parse(["pacman", "-Qgq", it]))
        return pkgs


def get_package_manager():
    platform_name = platform.linux_distribution()[0]
    if platform_name == "arch":
        return PacmanManager()
    else:
        raise NotImplementedError()


class Config(object):
    def __init__(self, path):
        if not os.path.isfile(path):
            path = os.path.join(os.getcwd(), path)
        config_data = {}
        exec(open(path).read(), config_data)
        self.packages = set(config_data["packages"])
        self.ignore_groups = set(config_data["ignore_groups"])


def gen_install_list(pkgs, gen_list=None, parent=None):
    if gen_list is None:
        gen_list = []
    if parent not in gen_list:
        for it in pkgs if parent is None else pkgs[parent]:
            if it not in gen_list:
                gen_install_list(pkgs, gen_list, it)

        if parent is not None:
            gen_list.append(parent)

    return gen_list


def gen_install_script(pkgs):
    return os.linesep.join(["yaourt -S --needed {0}".format(pkg)
                            for pkg in gen_install_list(pkgs)])

mng = get_package_manager()
cfg = Config("config.py")

pkgs = {}
for pkg in cfg.packages:
    pkgs[pkg] = mng.depend_packages(pkg).intersection(cfg.packages)
print(gen_install_script(pkgs))
# ignore_pkgs = mng.groups_depend_packages(cfg.ignore_groups)
# explicit_pkgs = mng.explicit_packages()
# new_pkgs = explicit_pkgs.difference(ignore_pkgs, cfg.packages)
# print(len(new_pkgs))
# print(new_pkgs)
# print(len(cfg.packages.intersection(ignore_pkgs)))
