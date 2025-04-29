from __future__ import division, print_function, absolute_import

__metaclass__ = type

from ansible.utils.display import Display
from ansible.plugins.action import ActionBase

display = Display()


class ActionModule(ActionBase):
    TRANSFERS_FILES = False

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        repo = self._task.args.get("repo")
        dest = self._task.args.get("dest")

        if not repo or not dest:
            result["failed"] = True
            result["msg"] = "Missing required arguments: repo and/or dest"
            return result

        module_return = self._execute_module(
            module_name="update_git", module_args={"repo": repo, "dest": dest}, task_vars=task_vars
        )

        if module_return.get("failed"):
            return module_return

        show_warning = module_return.get("show_warning")
        if show_warning:
            display.warning(show_warning)

        result.update(module_return)
        return result
