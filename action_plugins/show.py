import os
from traceback import format_exc
from ansible import constants as C
from ansible.plugins.action import ActionBase

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class StrError(RuntimeError):
    pass


# sample colors (default = COLOR_WARN):
# COLOR_HIGHLIGHT = "white"
# COLOR_VERBOSE = "blue"
# COLOR_WARN = "bright purple"
# COLOR_ERROR = "red"
# COLOR_DEBUG = "dark gray"
# COLOR_DEPRECATE = "purple"
# COLOR_SKIP = "cyan"
# COLOR_UNREACHABLE = "bright red"
# COLOR_OK = "green"
# COLOR_CHANGED = "yellow"
#
# show: msg="my text"
# show: msg="my text" color="white"
class ActionModule(ActionBase):
    TRANSFERS_FILES = False

    def _get_param_msg(self):
        param_name = "msg"
        result = self._task.args.get(param_name, None)
        if result is None or result.strip() == "":
            raise StrError("Not found required param '{}'.".format(param_name))

        return result.strip()

    def _get_param_color(self):
        param_name = "color"
        result = self._task.args.get(param_name, C.COLOR_WARN)
        if result is None or result.strip() == "":
            raise StrError("Not found required param '{}'.".format(param_name))

        return result.strip()

    @staticmethod
    def _print_exception(text):
        display.error(text, wrap_text=False)

    def _run(self):
        msg = self._get_param_msg()
        color = self._get_param_color()
        display.display("{}:".format(msg), color=color)

        return {"msg": msg, "changed": False}

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        try:
            result.update(self._run())
        except StrError as e:
            result['failed'] = True
            result['msg'] = "Error in action_plugin/show: " + str(e)
        except Exception:
            ActionModule._print_exception(format_exc())
            result['failed'] = True
            result['msg'] = "Error in action_plugin/show: "

        return result
