#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.text.converters import to_native


def get_version(module, git_path, dest) -> None | str:
    cmd = [git_path, "rev-parse", "HEAD"]
    rc, stdout, stderr = module.run_command(cmd, cwd=dest)
    if rc != 0:
        return None
    return to_native(stdout).strip()


def clone(module, git_path, repo, dest) -> None:
    dest_dirname = os.path.dirname(dest)
    if not os.path.exists(dest_dirname):
        os.makedirs(dest_dirname, exist_ok=True)

    cmd = [git_path, "clone", repo, dest]
    module.run_command(cmd, check_rc=True, cwd=dest_dirname)


def has_local_mods(module, git_path, dest) -> bool:
    cmd = [git_path, "status", "--porcelain"]
    rc, stdout, stderr = module.run_command(cmd, cwd=dest)
    if rc != 0:
        return False
    lines = stdout.splitlines()
    # Игнорируем untracked файлы (??)
    filtered = [l for l in lines if not l.startswith("??")]
    return len(filtered) > 0


def get_head_branch(module, git_path, dest) -> str:
    cmd = [git_path, "symbolic-ref", "--short", "-q", "HEAD"]
    rc, stdout, stderr = module.run_command(cmd, cwd=dest)
    if rc != 0:
        return "_not_a_branch"  # Detached HEAD
    return to_native(stdout).strip()


def pull_master(module, git_path, dest) -> bool:
    version_before = get_version(module, git_path, dest)
    cmd = [git_path, "pull", "origin", "master"]
    rc, stdout, stderr = module.run_command(cmd, cwd=dest)

    if rc != 0:
        module.fail_json(msg=f"Failed to pull master: {stderr}")

    version_after = get_version(module, git_path, dest)
    return version_before != version_after


def run_module() -> None:
    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(required=True, type="path"),
            repo=dict(required=True, type="str"),
        ),
        supports_check_mode=False,
    )

    dest = os.path.abspath(module.params["dest"])
    repo = module.params["repo"]
    git_path = module.get_bin_path("git", True)

    module.run_command_environ_update = dict(LANG="C", LC_ALL="C", LC_MESSAGES="C")

    result = {"changed": False}

    try:
        if not os.path.exists(dest):
            clone(module, git_path, repo, dest)
            result["changed"] = True
        else:
            if not os.path.exists(os.path.join(dest, ".git")):
                module.fail_json(
                    msg=f"Destination directory '{dest}' exists and is not a git repository"
                )

            if has_local_mods(module, git_path, dest):
                result["show_warning"] = f"Local modifications exist in repository ({dest})"
            elif get_head_branch(module, git_path, dest) != "master":
                result["show_warning"] = f"HEAD branch is not 'master' in repository ({dest})"
            else:
                if pull_master(module, git_path, dest):
                    result["changed"] = True

        module.exit_json(**result)

    except Exception as e:
        module.fail_json(msg=f"Unexpected error: {str(e)}")


if __name__ == "__main__":
    run_module()
