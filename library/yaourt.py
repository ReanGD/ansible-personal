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
from ansible.module_utils.basic import *

YAOURT_PATH = "/usr/bin/yaourt"
PACMAN_PATH = "/usr/bin/pacman"


def query_package(module, name, asexplicit):
    if asexplicit:
        lcmd = "pacman -Qie %s" % (name)
    else:
        lcmd = "pacman -Qi %s" % (name)
    lrc, lstdout, lstderr = module.run_command(lcmd, check_rc=False)
    return lrc == 0


def resolve_conflict(module, name):
    lcmd = "yaourt -Si %s" % (name)
    lrc, lstdout, lstderr = module.run_command(lcmd, check_rc=False)
    if lrc != 0:
        module.fail_json(msg="could not get package info")

    find_line = "Conflicts With :"
    conflicts = []
    for line in lstdout.split(os.linesep):
        if find_line in line:
            conflicts = line[len(find_line):].split()
        elif len(conflicts) != 0:
            if ":" not in line:
                conflicts += line.split()
            else:
                break

    if len(conflicts) == 0:
        return

    lcmd = "pacman -T %s" % (" ".join(conflicts))
    lrc, lstdout, lstderr = module.run_command(lcmd, check_rc=False)

    conflicts = list(set(conflicts).difference(set(lstdout.split())))
    if len(conflicts) == 0:
        return

    lcmd = "yaourt -Rs %s --noconfirm" % (" ".join(conflicts))
    lrc, lstdout, lstderr = module.run_command(lcmd, check_rc=False)
    if lrc != 0:
        msg = "could not remove packages (%s)" % (",".join(conflicts))
        module.fail_json(msg=msg)


def update_package_db(module):
    cmd = "yaourt -Sya"
    rc, stdout, stderr = module.run_command(cmd, check_rc=False)
    if rc == 0:
        return True
    else:
        module.fail_json(msg="could not update package db")


def install_packages(module, packages):
    install_c = 0

    for i, package in enumerate(packages):
        param_explicit = " --asexplicit"
        installed = query_package(module, package, False)
        if not installed:
            param_explicit = ""
        installed = query_package(module, package, True)
        if not installed:
            cmd = "yaourt -S %s %s --noconfirm" % (package, param_explicit)
            rc, stdout, stderr = module.run_command(cmd, check_rc=False)
            if rc != 0:
                msg = "failed to install %s" % (package)
                module.fail_json(stdout=stdout, stderr=stderr, msg=msg)
            install_c += 1

    if install_c != 0:
        msg = "installed %s package(s)" % (install_c)
        module.exit_json(changed=True, msg=msg)

    module.exit_json(changed=False, msg="package(s) already installed")


def check_packages(module, packages):
    would_be_changed = []
    for package in packages:
        if not query_package(module, package, True):
            would_be_changed.append(package)
    if would_be_changed:
        msg = "%s package(s) would be installed" % (len(would_be_changed))
        module.exit_json(changed=True, msg=msg)
    else:
        module.exit_json(change=False, msg="package(s) already installed")


def main():
    module = AnsibleModule(
        argument_spec=dict(
            name=dict(aliases=['pkg']),
            state=dict(default='present', choices=['present']),
            update_cache=dict(default='no', aliases=['update-cache'],
                              choices=BOOLEANS, type='bool')),
        required_one_of=[['name', 'update_cache']],
        supports_check_mode=True)

    if not os.path.exists(YAOURT_PATH):
        msg = "cannot find yaourt, looking for %s" % (YAOURT_PATH)
        module.fail_json(msg=msg)

    if not os.path.exists(PACMAN_PATH):
        msg = "cannot find pacman, looking for %s" % (PACMAN_PATH)
        module.fail_json(msg=msg)

    p = module.params

    if p["update_cache"] and not module.check_mode:
        update_package_db(module)
        if not p['name']:
            module.exit_json(changed=True,
                             msg='updated the package master lists')

    if p['update_cache'] and module.check_mode and not p['name']:
        module.exit_json(changed=True,
                         msg='Would have updated the package cache')

    if p['name']:
        pkgs = p['name'].split(',')
        if module.check_mode:
            check_packages(module, pkgs)

        if p['state'] in ['present']:
            for pkg in pkgs:
                resolve_conflict(module, pkg)
            install_packages(module, pkgs)


if __name__ == '__main__':
    main()
