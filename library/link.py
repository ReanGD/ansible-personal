#!/usr/bin/python2
# -*- coding: utf-8 -*-

DOCUMENTATION = '''
---
module: link
short_description: Create link (for config files and directories)
description:
    - Create link (for config files and directories).
version_added: "1.0"
author:
    - "'ReanGD (@novovladimir)'"
notes: []
requirements: []
options:
  src:
    description:
      - source path
    required: true
    default: null
  dst:
    description:
      - destination path
    required: true
    default: null
'''

EXAMPLES = '''
# create symlink from ~/dir1 to ~/dir2 and set: owner=foo group=foo for ~/dir2
- link: src=~/dir1 dst=~/dir2 owner=foo group=foo
'''

import os
import shutil
import os.path
from ansible.module_utils.basic import *


def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(aliases=['source'], default=None, required=True),
            dst=dict(aliases=['dest', 'destination'],
                     default=None, required=True)),
        add_file_common_args=True,
        supports_check_mode=True)

    src = os.path.abspath(os.path.expanduser(module.params['src']))
    dst = os.path.abspath(os.path.expanduser(module.params['dst']))
    module.params['path'] = dst
    file_args = module.load_file_common_arguments(module.params)

    exists = os.path.lexists(dst)
    changed = not (exists and os.path.islink(dst) and os.readlink(dst) == src)
    if not module.check_mode:
        if changed:
            try:
                if exists:
                    if os.path.isdir(dst):
                        shutil.rmtree(dst, ignore_errors=False)
                    else:
                        os.unlink(dst)
                os.symlink(src, dst)
            except Exception as e:
                module.fail_json(msg="operation failed: %s " % str(e))
        changed = module.set_fs_attributes_if_different(file_args, changed)

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
