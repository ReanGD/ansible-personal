# -*- coding: utf-8 -*-
import sys
import os.path
import subprocess
from ansible.errors import *
from ansible.plugins.lookup import LookupBase


class PackageManager:
    PACMAN_PATH = "/usr/bin/pacman"
    YAOURT_PATH = "/usr/bin/yaourt"
    
    def __init__(self):
        self._check_path()
        self._rc = 0

    def _check_path(self):
        if not os.path.exists(PackageManager.PACMAN_PATH):
            raise AnsibleError("cannot find pacman, looking for %s" % PackageManager.PACMAN_PATH)
        if not os.path.exists(PackageManager.YAOURT_PATH):
            raise AnsibleError("cannot find yaourt, looking for %s" % PackageManager.YAOURT_PATH)

    def __parse(self, cmd, hide_stderr = False):
        if hide_stderr:
            stderr = subprocess.PIPE
        else:
            stderr = None
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=stderr)
        out, err = p.communicate()
        self._rc = p.returncode
        return set(out.decode("UTF-8").split())

    def all_installed_packages(self):
        return self.__parse([PackageManager.PACMAN_PATH, "-Qq"])

    def explicit_installed_packages(self):
        return self.__parse([PackageManager.PACMAN_PATH, "-Qeq"])

    def is_exists_package(self, name):
        self.__parse([PackageManager.YAOURT_PATH, "-Si", name], hide_stderr=True)
        return self._rc == 0

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

        if not os.path.exists(config_path):
            raise AnsibleError('config file "%s" not found' % config_path)
        try:
            if sys.version_info[0] == 3:
                exec(open(config_path).read(), self.gvars)
            else:
                execfile(config_path, self.gvars)
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
            'action': "not_installed",
        }
        avaible_actions = ["not_installed", "new", "error"]

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

    def action_not_installed(self):
        installed_packages = self.__installed()
        ignored_packages = self.__ignored()
        packages = installed_packages.difference(ignored_packages)
        explicit_packages = self.mng.explicit_installed_packages()
        result = packages.difference(explicit_packages)

        return list(result)

    def action_new(self, existing):
        installed_packages = self.__installed()
        ignored_packages = self.__ignored()
        explicit_packages = self.mng.explicit_installed_packages()
        result = explicit_packages.difference(installed_packages, ignored_packages)
        result = [it for it in result if self.mng.is_exists_package(it) == existing]

        return result


    def run(self, terms, variables=None, **kwargs):
        params = self.__parse_terms(terms)
        action = params['action']
        basedir = self.get_basedir(variables)
        full_path = os.path.join(basedir, "vars", params["path"])
        self.cfg = UserConfig(full_path, params["host"])
        self.mng = PackageManager()

        if action == "not_installed":
            return self.action_not_installed()
        elif action == "new":
            return self.action_new(True)
        elif action == "error":
            return self.action_new(False)
        else:
            raise AnsibleError("error action (%s)" % action)
