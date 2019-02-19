import os
import shutil
from ansible.module_utils.basic import AnsibleModule


def main():
    module = AnsibleModule(
        argument_spec=dict(
            src=dict(default=None, required=True, type="path"),
            dst=dict(default=None, required=True, type="path"),
            ),
        add_file_common_args=True,
        supports_check_mode=False
    )

    src = os.path.abspath(os.path.expanduser(module.params['src']))
    dst = os.path.abspath(os.path.expanduser(module.params['dst']))

    exists = os.path.lexists(dst)
    changed = not (exists and os.path.islink(dst) and os.readlink(dst) == src)

    if changed:
        try:
            if exists:
                if os.path.isdir(dst):
                    shutil.rmtree(dst, ignore_errors=False)
                else:
                    os.unlink(dst)
            os.symlink(src, dst)
        except Exception as e:
            module.fail_json(msg="operation failed: {}".format(str(e)))

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
