# -*- coding: utf-8 -*-
import sys
import os.path
import subprocess
from ansible.errors import *


PACMAN_PATH = "/usr/bin/pacman"


class PacmanManager:
    def __init__(self):
        if not os.path.exists(PACMAN_PATH):
            raise AnsibleError('not fount pacman package')

    def __parse(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()
        return set(out.decode("UTF-8").split())

    def all_installed_packages(self):
        return self.__parse([PACMAN_PATH, "-Qq"])

    def explicit_installed_packages(self):
        return self.__parse([PACMAN_PATH, "-Qeq"])

    def group_members(self, group):
        return self.__parse([PACMAN_PATH, "-Qgq", group])

    def groups_members(self, groups):
        pkgs = set()
        for it in groups:
            pkgs.update(self.group_members(it))
        return pkgs


class UserConfig:
    def __init__(self, config_path):
        self.config_data = {}
        full_path = os.path.expanduser(config_path)
        if not os.path.exists(full_path):
            raise AnsibleError('config file "%s" not found' % full_path)
        try:
            execfile(os.path.expanduser(full_path), self.config_data)
        except:
            e = sys.exc_info()[1]
            raise AnsibleError(e)

    def __getitem__(self, item):
        return set(self.config_data[item])


class LookupModule:
    def __init__(self, **kwargs):
        self.cfg = None
        self.mng = None

    def __parse_terms(self, terms):
        params = terms.split()
        config_path = params[0]
        paramvals = {
            'action': "all",
        }
        avaible_actions = ['all', 'not_installed', 'new']

        try:
            for param in params[1:]:
                name, value = param.split('=')
                assert(name in paramvals)
                paramvals[name] = value
            assert(paramvals['action'] in avaible_actions)
        except (ValueError, AssertionError) as e:
            raise AnsibleError(e)

        paramvals['path'] = config_path
        return paramvals

    def __ignored(self):
        ignore_groups = self.cfg["ignore_groups"]
        ignore_packages = self.mng.groups_members(ignore_groups)
        ignore_packages.update(self.cfg["ignore_packages"])

        return ignore_packages

    def action_all(self):
        packages = self.cfg["packages"]
        ignored_packages = self.__ignored()
        ret = packages.difference(ignored_packages)

        return list(ret)

    def action_not_installed(self):
        packages = self.cfg["packages"]
        ignored_packages = self.__ignored()
        explicit_packages = self.mng.explicit_installed_packages()
        ret = packages.difference(ignored_packages, explicit_packages)

        return list(ret)

    def action_new(self):
        packages = self.cfg["packages"]
        ignored_packages = self.__ignored()
        explicit_packages = self.mng.explicit_installed_packages()
        ret = explicit_packages.difference(packages, ignored_packages)

        return list(ret)

    def run(self, terms, variables=None, **kwargs):
        params = self.__parse_terms(terms)
        action = params['action']
        self.cfg = UserConfig(params['path'])
        self.mng = PacmanManager()

        if action == "all":
            return self.action_all()
        elif action == "not_installed":
            return self.action_not_installed()
        elif action == "new":
            return self.action_new()
        else:
            raise AnsibleError("error action (%s)" % action)
