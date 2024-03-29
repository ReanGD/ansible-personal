from traceback import format_exc
from ansible.plugins.action import ActionBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class Clr:
    COLOR_HIGHLIGHT = 'white'
    COLOR_VERBOSE = 'blue'
    COLOR_WARN = 'bright purple'
    COLOR_ERROR = 'red'
    COLOR_DEBUG = 'dark gray'
    COLOR_DEPRECATE = 'purple'
    COLOR_SKIP = 'cyan'
    COLOR_UNREACHABLE = 'bright red'
    COLOR_OK = 'green'
    COLOR_CHANGED = 'yellow'


class StrError(RuntimeError):
    pass


class ActionModule(ActionBase):
    TRANSFERS_FILES = False

    def _get_param_dest(self):
        param_name = "dest"
        result = self._task.args.get(param_name, None)
        if result is None or result.strip() == "":
            raise StrError("Not found required param '{}'.".format(param_name))

        return result.strip()

    def _get_param_repo(self):
        param_name = "repo"
        result = self._task.args.get(param_name, None)
        if result is None or result.strip() == "":
            raise StrError("Not found required param '{}'.".format(param_name))

        return result.strip()

    @staticmethod
    def _print_exception(text):
        display.error(text, wrap_text=False)

    @staticmethod
    def _print_warning(text):
        display.display(text, color=Clr.COLOR_WARN)

    def _call_module(self, name, args):
        result = self._execute_module(module_name=name, module_args=args,
                                      task_vars=self._task_vars)
        if result.get("failed"):
            exception = result.get("exception", None)
            if exception is not None:
                self._print_exception(exception)

            msg = result.get("msg", "Unknown error in module {}".format(name))
            raise StrError("lib error: {}".format(msg))

        return result

    def _run(self):
        args = {"dest": self._get_param_dest(), "repo": self._get_param_repo()}
        result = self._call_module(name="update_git", args=args)

        show_warning = result.get("show_warning")
        if show_warning is not None:
            self._print_warning(show_warning)

        return result

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        self._supports_async = False
        self._supports_check_mode = False
        result = super(ActionModule, self).run(tmp, task_vars)
        del tmp  # tmp no longer has any effect

        self._task_vars = task_vars
        try:
            result.update(self._run())
        except StrError as e:
            result['failed'] = True
            result['msg'] = str(e)
        except Exception:
            ActionModule._print_exception(format_exc())
            result['failed'] = True
            result['msg'] = "Error in action_plugin/update_git: "

        return result
