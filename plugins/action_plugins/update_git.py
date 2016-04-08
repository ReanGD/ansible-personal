import os
import re
import sys
from ansible.plugins.action import ActionBase, display

module_dir = os.path.dirname(os.path.abspath(__file__))
if module_dir not in sys.path:
    sys.path.append(module_dir)
from helper import BaseActionModule


class ActionModule(ActionBase, BaseActionModule):
    def run(self, tmp=None, task_vars=None):
        return self.base_run(ActionModule, task_vars, ['repo', 'dest'])

    def impl(self, repo, dest):
        self.repo = repo
        self.dest = os.path.abspath(os.path.expanduser(dest))
        self.run_command_environ_update = dict(LANG='C', LC_ALL='C', LC_MESSAGES='C', LC_CTYPE='C')
        self.git = self.get_bin_path('git', True)

        if self.try_clone():
            self.exit_changed()
        else:
            if not self.is_under_git():
                self.exit_failed('dest directory \'%s\' is not empty' % self.dest)
            elif self.has_local_mods():
                display.warning('Local modifications exist in repository (%s).\n\n' % dest)
            elif self.get_head_branch() != 'master':
                display.warning('HEAD branch not a master in repository (%s).\n\n' % dest)
            elif self.get_remote_head() != self.get_local_head():
                self.pull()
                self.exit_changed()

    def is_under_git(self):
        gitconfig = os.path.join(self.dest, '.git', 'config')
        return os.path.isfile(gitconfig)

    def has_local_mods(self):
        cmd = '%s status -s' % (self.git)
        rc, stdout, stderr = self.run_command(cmd, cwd=self.dest)
        lines = stdout.splitlines()
        lines = filter(lambda c: not re.search('^\\?\\?.*$', c), lines)

        return len(lines) > 0

    def get_branches(self):
        branches = []
        cmd = '%s branch -a' % (self.git,)
        (rc, out, err) = self.run_command(cmd, cwd=self.dest)
        if rc != 0:
            self.exit_failed('Could not determine branch data - received %s' % out)
        for line in out.split('\n'):
            branches.append(line.strip())
        return branches

    def is_not_a_branch(self):
        branches = self.get_branches()
        for b in branches:
            if b.startswith('* ') and ('no branch' in b or 'detached from' in b):
                return True
        return False

    def get_head_branch(self):
        repo_path = os.path.join(self.dest, '.git')
        # Read .git/HEAD for the name of the branch.
        # If we're in a detached HEAD state, look up the branch associated with
        # the remote HEAD in .git/refs/remotes/origin/HEAD
        f = None
        if self.is_not_a_branch():
            f = open(os.path.join(repo_path, 'refs', 'remotes', 'origin', 'HEAD'))
        else:
            f = open(os.path.join(repo_path, 'HEAD'))
        branch = f.readline().split('/')[-1].rstrip('\n')
        f.close()
        return branch

    def get_remote_head(self):
        cmd = '%s ls-remote origin -h HEAD' % (self.git,)
        (rc, out, err) = self.run_command(cmd, check_rc=True, cwd=self.dest)
        if len(out) < 1:
            self.exit_failed('Could not determine remote revision')
        rev = out.split()[0]
        return rev

    def get_local_head(self):
        cmd = '%s rev-parse HEAD' % (self.git, )
        rc, stdout, stderr = self.run_command(cmd, cwd=self.dest)
        sha = stdout.rstrip('\n')
        return sha

    def try_clone(self):
        if os.path.isdir(self.dest) and os.listdir(self.dest):
            return False
        self.dest_dirname = os.path.dirname(self.dest)
        try:
            os.makedirs(self.dest_dirname)
        except:
            pass
        cmd = [ self.git, 'clone', self.repo, self.dest ]
        self.run_command(cmd, check_rc=True, cwd=self.dest_dirname)
        return True

    def pull(self):
        cmd = [ self.git, 'pull', 'origin', 'master' ]
        self.run_command(cmd, cwd=self.dest)
