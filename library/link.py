import os
import shutil
from ansible.module_utils.basic import AnsibleModule


def copytree(src, dst):
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
            is_symlink = srcentry.is_symlink()
            if is_symlink:
                linkto = os.readlink(srcname)
                if not os.path.exists(linkto):
                    continue

                if srcentry.is_dir():
                    copytree(srcentry, dstname)
                else:
                    shutil.copy2(srcentry, dstname)
            elif srcentry.is_dir():
                copytree(srcentry, dstname)
            else:
                # Will raise a SpecialFileError for unsupported file types
                shutil.copy2(srcentry, dstname)
        # catch the Error from the recursive copytree so that we can
        # continue with other files
        except shutil.Error as err:
            errors.extend(err.args[0])
        except OSError as why:
            errors.append((srcname, dstname, str(why)))

    try:
        shutil.copystat(src, dst)
    except OSError as why:
        # Copying file access times may fail on Windows
        if getattr(why, 'winerror', None) is None:
            errors.append((src, dst, str(why)))

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

    exists = os.path.lexists(dst)
    exists_dir = os.path.isdir(dst)
    changed = not (exists and os.path.islink(dst) and os.readlink(dst) == src)

    if changed:
        try:
            if exists_dir:
                os.rename(dst, dst_backup)
            elif exists:
                os.unlink(dst)

            os.symlink(src, dst)

            if exists_dir:
                copytree(dst_backup, dst)
                shutil.rmtree(dst_backup, ignore_errors=False)

        except Exception as e:
            module.fail_json(msg="operation failed: {}".format(str(e)))

    module.exit_json(changed=changed)


if __name__ == '__main__':
    main()
