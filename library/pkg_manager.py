import os
import zlib
import traceback
from subprocess import run
from ansible.module_utils.urls import open_url
from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
import ansible.module_utils.six.moves.urllib.error as urllib_error
from ansible.module_utils.urls import fetch_url, url_argument_spec


class PkgManager:
    def run(self, params):
        res = run(["/usr/bin/pacman"] + params, capture_output=True)
        res.check_returncode()
        return {it.strip() for it in res.stdout.decode("utf-8").split('\n') if it.strip() != ""}

    def is_run_success(self, params):
        res = run(["/usr/bin/pacman"] + params, capture_output=True)
        return not res.returncode

    def get_db_groups(self):
        return self.run(["-Sg"])

    def get_db_packages(self):
        return self.run(["-Slq"])

    def get_aur_packages(self):
        url = "https://aur.archlinux.org/packages.gz"
        try:
            text_gz = open_url(url).read()
            text = zlib.decompress(text_gz, 16 + zlib.MAX_WBITS).decode("utf-8")
            return {it.strip() for it in text.split() if it.strip() != ""}
        except urllib_error.HTTPError as e:
            raise RuntimeError("Error connect to '{}', error = {}".format(url, to_native(e)))        

    def get_local_packages(self):
        return self.run(["-Qq"])

    def get_local_explicit_packages(self):
        return self.run(["-Qeq"])

    def get_db_packages_for_groups(self, group_names):
        if len(group_names) == 0:
            return set()

        return { line.split()[1] for line in self.run(["-Sg"] + list(group_names)) }

    def get_local_packages_for_groups(self, group_names):
        if len(group_names) == 0:
            return set()

        return { line.split()[1] for line in self.run(["-Qg"] + list(group_names)) }


def install_makepkg(pkg_name):
    pkg_name = pkg_name.strip()

    msg = "{}: success".format(pkg_name)
    return msg, True


def install_pacman(pkg_name):
    pkg_name = pkg_name.strip()

    msg = "{}: success".format(pkg_name)
    return msg, True


def install_yay(pkg_name):
    pkg_name = pkg_name.strip()

    msg = "{}: success".format(pkg_name)
    return msg, True


def get_info(packages, groups):
    # ошибочные названия среди groups (groups_name_wrong)
    # ошибочные названия среди packages (packages_name_wrong)
    # неустановленные среди packages (packages_not_installed)
    # установленные как не explicit среди packages (packages_not_explicit)
    # новые explicit пакеты, которых нет среди packages и пакетов groups (packages_new)
    # пакеты среди packages, которые находятся в aur (packages_aur)
    # пакеты среди packages, которые относятся к пакетам в groups (packages_in_group)
    # пакеты входящие в groups, но не установленные (packages_not_installed_in_group)

    packages = {it.strip() for it in packages}
    groups = {it.strip() for it in groups}
    mng = PkgManager()

    db_groups = mng.get_db_groups()
    db_packages = mng.get_db_packages()
    aur_packages = mng.get_aur_packages()
    local_packages = mng.get_local_packages()
    local_explicit_packages = mng.get_local_explicit_packages()
    db_packages_for_groups = mng.get_db_packages_for_groups(groups)
    local_packages_for_groups = mng.get_local_packages_for_groups(groups)

    groups_name_wrong = groups.difference(db_groups)
    packages_name_wrong = packages.difference(db_packages, aur_packages)
    packages_not_installed = packages.difference(local_packages)
    packages_not_explicit = packages.difference(local_explicit_packages)
    packages_new = local_explicit_packages.difference(packages, local_packages_for_groups)
    packages_aur = aur_packages.intersection(packages)
    packages_in_group = local_packages_for_groups.intersection(packages)
    packages_not_installed_in_group = db_packages_for_groups.difference(local_packages_for_groups)

    return {
        "groups_name_wrong": list(groups_name_wrong),
        "packages_name_wrong": list(packages_name_wrong),
        "packages_not_installed": list(packages_not_installed),
        "packages_not_explicit": list(packages_not_explicit),
        "packages_new": list(packages_new),
        "packages_aur": list(packages_aur),
        "packages_in_group": list(packages_in_group),
        "packages_not_installed_in_group": list(packages_not_installed_in_group),
    }

# pkg_manager: command=install name=yay use=makepkg
# pkg_manager: command=install name=python use=pacman
# pkg_manager: command=install name=dropbox use=yay
# pkg_manager: command=get_info packages=python2,python groups=base
def main():
    module = AnsibleModule(
        argument_spec=dict(
            command=dict(default=None, choices=["install", "get_info"], required=True, type="str"),
            name=dict(default=None, required=False, type="str"),
            use=dict(default="yay", choices=["makepkg", "pacman", "yay"], required=False, type="str"),
            packages=dict(default=None, required=False, type="list"),
            groups=dict(default=None, required=False, type="list")
            ),
        supports_check_mode=False)
    command = module.params["command"].strip()

    if command == "install":
        name = module.params.get("name", None)
        use = module.params.get("use", "yay").strip()
        if name is None or name.strip() == "":
            module.fail_json(msg="Not found required param 'name' for command 'install'")
        elif use not in ["makepkg", "pacman", "yay"]:
            module.fail_json(msg="Param 'use' has unexpected value '{}' for command 'install'".format(use))
        else:
            try:
                name = name.strip()
                if use == "makepkg":
                    msg, changed = install_makepkg(name)
                elif use == "pacman":
                    msg, changed = install_pacman(name)
                else:
                    msg, changed = install_yay(name)
                module.exit_json(msg=msg, changed=changed, package=name)
            except Exception as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
    elif command == "get_info":
        packages = module.params.get("packages", None)
        groups = module.params.get("groups", None)
        if packages is None:
            module.fail_json(msg="Not found required param 'packages' for command '{}'".format(command))
        elif groups is None:
            module.fail_json(msg="Not found required param 'groups' for command '{}'".format(command))
        else:
            try:
                result = get_info(packages, groups)
                module.exit_json(**result)
            except Exception as e:
                module.fail_json(msg=to_native(e), exception=traceback.format_exc())
    else:
        module.fail_json(msg="Param 'command' has unexpected value '{}'".format(command))


if __name__ == '__main__':
    main()
