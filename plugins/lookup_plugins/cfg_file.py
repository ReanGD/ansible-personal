# -*- coding: utf-8 -*-
import sys
import os.path
import subprocess
from ansible.errors import *
from ansible.plugins.lookup import LookupBase

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
    def __init__(self, config_path, host):
        self.gvars = {'host': host}
        full_path = os.path.expanduser(config_path)
        if not os.path.exists(full_path):
            raise AnsibleError('config file "%s" not found' % full_path)
        try:
            execfile(full_path, self.gvars)
        except:
            e = sys.exc_info()[1]
            raise AnsibleError(e)

    def __getitem__(self, item):
        return set(self.gvars[item])


class LookupModule(LookupBase):
    def __init__(self, **kwargs):
        self.cfg = None
        self.mng = None

    def __parse_terms(self, terms):
        params = terms[0].split()
        config_path = params[0]
        paramvals = {
            'host': '',
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
        self.cfg = UserConfig(params['path'], params['host'])
        self.mng = PacmanManager()

        if action == "all":
            return self.action_all()
        elif action == "not_installed":
            return self.action_not_installed()
        elif action == "new":
            return self.action_new()
        else:
            raise AnsibleError("error action (%s)" % action)
