import os
import shutil
from ansible.module_utils.basic import AnsibleModule


def copytree(src, dst, need_copystat):
    with os.scandir(src) as itr:
        entries = list(itr)

    if not os.path.isdir(dst):
        os.makedirs(dst, exist_ok=False)

    errors = []
    for srcentry in entries:
        srcname = os.path.join(src, srcentry.name)
        dstname = os.path.join(dst, srcentry.name)
        if os.path.exists(dstname):
            continue

        try:
            if srcentry.is_symlink() and not os.path.exists(os.readlink(srcname)):
                continue

            if srcentry.is_dir():
                copytree(srcentry, dstname, True)
            else:
                shutil.copy2(srcentry, dstname)
        except shutil.Error as err:
            # catch the Error from the recursive copytree so that we can continue with other files
            errors.extend(err.args[0])
        except OSError as why:
            errors.append((srcname, dstname, str(why)))

    try:
        if need_copystat:
            shutil.copystat(src, dst)
    except OSError as why:
        errors.append((src, dst, f"copystat: {why}"))

    if errors:
        raise shutil.Error(errors)


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
    dst_backup = dst + "__"

    dst_exists = os.path.lexists(dst)
    dst_dir_exists = os.path.isdir(dst)
    dst_dir_exists_and_empty = dst_dir_exists and (len(os.listdir(dst)) == 0)
    changed = not (dst_exists and os.path.islink(dst) and os.readlink(dst) == src)

    if changed:
        try:
            if dst_dir_exists_and_empty:
                shutil.rmtree(dst, ignore_errors=False)
            elif dst_dir_exists:
                os.rename(dst, dst_backup)
            elif dst_exists:
                os.unlink(dst)

            os.symlink(src, dst)

            if dst_dir_exists and not dst_dir_exists_and_empty:
                copytree(dst_backup, dst, False)
                shutil.rmtree(dst_backup, ignore_errors=False)

        except Exception as e:
            module.fail_json(msg="operation failed: {}".format(str(e)))

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
