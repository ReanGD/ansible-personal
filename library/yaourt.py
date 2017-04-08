#!/usr/bin/python2
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: yaourt
short_description: Manage packages with I(yaourt)
description:
    - Manage packages with the I(yaourt) package manager, which is used by
      Arch Linux and its variants.
version_added: "1.0"
author:
    - "'ReanGD (@novovladimir)'"
notes: []
requirements: []
options:
    name:
        description:
            - Name of the package to install.
        required: false
        default: null

    state:
        description:
            - Desired state of the package.
        required: false
        default: "present"
        choices: ["present"]

    update_cache:
        description:
            - Whether or not to refresh the master package lists. This can be
              run as part of a package installation or as a separate step.
        required: false
        default: "no"
        choices: ["yes", "no"]
'''

EXAMPLES = '''
# Install package foo
- yaourt: name=foo state=present

# Run the equivalent of "yaourt -Sya" as a separate step
- yaourt: update_cache=yes
'''

import os
import os.path
import ansible.module_utils.basic


# ansible.module_utils.basic._ANSIBLE_ARGS = '{"ANSIBLE_MODULE_ARGS":{}}'.encode('utf-8')

class PackageManager:
    YAOURT_PATH = "/usr/bin/yaourt"
    PACMAN_PATH = "/usr/bin/pacman"

    def __init__(self, ansible_module):
        self.module = ansible_module
        self._check_path()

    def fail(self, msg):
        self.module.fail_json(msg=msg)

    def _run(self, cmd, raise_msg):
        rc, stdout, stderr = module.run_command(cmd, check_rc=False)
        lines = [it for it in stdout.split(os.linesep) if it.strip()]
        if rc != 0:
            if raise_msg:
                msg = "Command: {}, exit code: {}, stdout: {}. stderr: {}"
                self.fail(msg.format(cmd, rc, stdout, stderr))
            else:
                return lines, False

        if raise_msg:
            return lines
        else:
            return lines, True

    def yaourt(self, params, raise_msg=True):
        return self._run(PackageManager.YAOURT_PATH + " " + params, raise_msg)

    def pacman(self, params, raise_msg=True):
        return self._run(PackageManager.PACMAN_PATH + " " + params, raise_msg)

    def _check_path(self):
        if not os.path.exists(PackageManager.YAOURT_PATH):
            self.fail("cannot find yaourt, looking for %s" % PackageManager.YAOURT_PATH)

        if not os.path.exists(PackageManager.PACMAN_PATH):
            self.fail("cannot find pacman, looking for %s" % PackageManager.PACMAN_PATH)

    def update_package_db(self):
        self.yaourt("-Syua")

    def _remove_conflict(self, name):
        find_line = "Conflicts With :"
        conflicts = []
        for line in self.yaourt("-Si " + name):
            if find_line in line:
                conflicts = line[len(find_line):].split()
            elif len(conflicts) != 0:
                if ":" not in line:
                    conflicts += line.split()
                else:
                    break

        if len(conflicts) == 0:
            return

        lines = self.pacman("-T " + " ".join(conflicts))
        if len(lines) != 0:
            not_installed_conflicts = set(lines[0].split())
        else:
            not_installed_conflicts = set()
        for_remove = list(set(conflicts).difference(not_installed_conflicts))
        if len(conflicts) != 0:
            self.pacman("-Rs %s --noconfirm" % (" ".join(for_remove)))

    def group_packages(self, group_name):
        return [it.split()[0].split('/')[1] for it in self.yaourt("-Sg " + group_name[1:])]

    def is_group(self, name):
        return name.startswith(":")

    def is_installed_asexplicit(self, name):
        _, success = self.pacman("-Qie " + name, raise_msg=False)
        return success

    def install_packages(self, raw_packages):
        packages = []
        for package in raw_packages:
            if self.is_group(package):
                packages += group_packages(package)
            else:
                packages.append(package)

        for package in packages:
            self._remove_conflict(package)

        for_install = [it for it in packages if not self.is_installed_asexplicit(it)]
        for package in for_install:
            self.yaourt("-S %s --asexplicit --noconfirm" % package)

        if len(for_install) != 0:
            msg = "installed %s package(s)" % (len(for_install))
            self.module.exit_json(changed=True, msg=msg)

        self.module.exit_json(changed=False, msg="package(s) already installed")


def main():
    ansible_module = ansible.module_utils.basic.AnsibleModule(
        argument_spec=dict(
            name=dict(aliases=['pkg']),
            state=dict(default='present', choices=['present']),
            update_cache=dict(default='no', aliases=['update-cache'],
                              choices=BOOLEANS, type='bool')),
        required_one_of=[['name', 'update_cache']],
        supports_check_mode=True)

    p = module.params
    pm = PackageManager(ansible_module)
    if p["update_cache"]:
        pm.update_package_db()
    elif p['name'] and p['state'] in ['present']:
        pm.install_packages(p['name'].split(','))


if __name__ == '__main__':
    main()
