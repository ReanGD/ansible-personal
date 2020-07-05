import os
import re
from traceback import format_exc
from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils._text import to_native


class StrError(RuntimeError):
    pass


def head_splitter(headfile, module):
    res = None
    if os.path.exists(headfile):
        rawdata = None
        try:
            f = open(headfile, 'r')
            rawdata = f.readline()
            f.close()
        except:
            raise StrError("Unable to read '{}'".format(headfile))
        if rawdata:
            try:
                rawdata = rawdata.replace("refs/remotes/origin", "", 1)
                refparts = rawdata.split(" ")
                newref = refparts[-1]
                nrefparts = newref.split("/", 2)
                res = nrefparts[-1].rstrip("\n")
            except:
                raise StrError("Unable to split head from '{}'".format(rawdata))
    return res


def get_version(module, git_path, dest):
    cmd = [git_path, "rev-parse", "HEAD"]
    rc, stdout, stderr = module.run_command(cmd, cwd=dest)
    sha = to_native(stdout).rstrip('\n')
    return sha


def clone(git_path, module, repo, dest):
    dest_dirname = os.path.dirname(dest)
    try:
        os.makedirs(dest_dirname)
    except:
        pass
    cmd = [git_path, "clone", repo, dest]
    module.run_command(cmd, check_rc=True, cwd=dest_dirname)


def has_local_mods(module, git_path, dest):
    cmd = [git_path, "status", "--porcelain"]
    rc, stdout, stderr = module.run_command(cmd, cwd=dest)
    lines = stdout.splitlines()
    lines = list(filter(lambda c: not re.search('^\\?\\?.*$', c), lines))

    return len(lines) > 0


def get_branches(git_path, module, dest):
    branches = []
    cmd = [git_path, "branch", "--no-color", "-a"]
    (rc, out, err) = module.run_command(cmd, cwd=dest)
    if rc != 0:
        raise StrError("Could not determine branch data, stdout: {}, stderr: {}, rc: {}".format(out, err, rc))
    for line in out.split('\n'):
        if line.strip():
            branches.append(line.strip())
    return branches


def is_not_a_branch(git_path, module, dest):
    branches = get_branches(git_path, module, dest)
    for branch in branches:
        if branch.startswith("* ") and ("no branch" in branch or
                                        "detached from" in branch or
                                        "detached at" in branch):
            return True
    return False


def get_head_branch(git_path, module, dest):
    if is_not_a_branch(git_path, module, dest):
        return "_not_a_branch"
    headfile = os.path.join(dest, ".git", "HEAD")
    branch = head_splitter(headfile, module)
    return branch


def pull_master(git_path, module, dest):
    version_before = get_version(module, git_path, dest)
    cmd = [git_path, 'pull', 'origin', 'master']
    (rc, out, err) = module.run_command(cmd, cwd=dest)
    if rc != 0:
        raise StrError("Failed to pull branch master, stdout: {}, stderr: {}, rc: {}".format(out, err, rc))

    return version_before != get_version(module, git_path, dest)


def run_module(module):
    dest = os.path.abspath(module.params['dest'])
    repo = module.params['repo']
    git_path = module.get_bin_path('git', True)
    is_dest = os.path.exists(dest)
    result = {"changed": False}

    module.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')

    if is_dest and not os.path.exists(os.path.join(dest, ".git", 'config')):
        raise StrError("Dest directory '{}', is not empty".format(dest))
    elif not is_dest:
        clone(git_path, module, repo, dest)
        result.update(changed=True)
    elif has_local_mods(module, git_path, dest):
        result.update(show_warning="Local modifications exist in repository ({})".format(dest))
    elif get_head_branch(git_path, module, dest) != 'master':
        result.update(show_warning="HEAD branch not a master in repository ({})".format(dest))
    elif pull_master(git_path, module, dest):
        result.update(changed=True)

    return result

# update_git: repo=git@github.com:User/Repo dest=/home/repodir
def main():
    module = AnsibleModule(
        argument_spec=dict(
            dest=dict(default=None, required=True, type="path"),
            repo=dict(default=None, required=True, type="str"),
            ),
        supports_check_mode=False
    )

    result = {}
    try:
        result = run_module(module)
    except StrError as e:
        result.update(failed=True, msg="Error in library/update_git: !!!")
        # result.update(failed=True, msg="Error in library/update_git: " + str(e))
        # module.fail_json(msg="Error in library/update_git: " + str(e))
    except Exception:
        result.update(failed=True, msg="Error in library/update_git: !!!")
        # result.update(failed=True, msg="Exception in library/update_git", exception=format_exc())
        # module.fail_json(msg="Exception in library/update_git", exception=format_exc())

    module.exit_json(**result)


if __name__ == '__main__':
    main()
