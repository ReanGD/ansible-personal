# -*- coding: utf-8 -*-
import sys
import os.path
import subprocess
from ansible.errors import *
from ansible.plugins.lookup import LookupBase


class PackageManager:
    PACMAN_PATH = "/usr/bin/pacman"
    
    def __init__(self):
        self._check_path()

    def _check_path(self):
        if not os.path.exists(PackageManager.PACMAN_PATH):
            raise AnsibleError("cannot find pacman, looking for %s" % PackageManager.PACMAN_PATH)

    def __parse(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        out, err = p.communicate()
        return set(out.decode("UTF-8").split())

    def all_installed_packages(self):
        return self.__parse([PackageManager.PACMAN_PATH, "-Qq"])

    def explicit_installed_packages(self):
        return self.__parse([PackageManager.PACMAN_PATH, "-Qeq"])

    def group_members(self, group, local):
        if local:
            params = "-Qgq"
        else:
            params = "-Sgq"
        return self.__parse([PackageManager.PACMAN_PATH, params, group])

    def groups_members(self, groups, local):
        pkgs = set()
        for it in groups:
            pkgs.update(self.group_members(it, local))
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

    def __installed(self):
        groups = self.cfg["groups"]
        packages = self.mng.groups_members(groups, False)
        packages.update(self.cfg["packages"])

        return packages

    def __ignored(self):
        groups = self.cfg["ignore_groups"]
        packages = self.mng.groups_members(groups, True)
        packages.update(self.cfg["ignore_packages"])

        return packages

    def action_all(self):
        packages = self.__installed()
        ignored_packages = self.__ignored()
        result = packages.difference(ignored_packages)

        return result

    def action_not_installed(self):
        packages = self.action_all()
        explicit_packages = self.mng.explicit_installed_packages()
        result = packages.difference(explicit_packages)

        return result

    def action_new(self):
        packages = self.action_all()
        explicit_packages = self.mng.explicit_installed_packages()
        result = explicit_packages.difference(packages)

        return result

    def run(self, terms, variables=None, **kwargs):
        params = self.__parse_terms(terms)
        action = params['action']
        self.cfg = UserConfig(params['path'], params['host'])
        self.mng = PackageManager()

        if action == "all":
            return list(self.action_all())
        elif action == "not_installed":
            return list(self.action_not_installed())
        elif action == "new":
            return list(self.action_new())
        else:
            raise AnsibleError("error action (%s)" % action)
