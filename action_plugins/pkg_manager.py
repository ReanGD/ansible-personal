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


# pkg_manager: command=get_info config={{packages_file}} host={{hostname_id}}
class ActionModule(ActionBase):
    # COLOR_HIGHLIGHT = 'white'
    # COLOR_VERBOSE = 'blue'
    # COLOR_WARN = 'bright purple'
    # COLOR_ERROR = 'red'
    # COLOR_DEBUG = 'dark gray'
    # COLOR_DEPRECATE = 'purple'
    # COLOR_SKIP = 'cyan'
    # COLOR_UNREACHABLE = 'bright red'
    # COLOR_OK = 'green'
    # COLOR_CHANGED = 'yellow'
    # def _install_pkg(self, pkg_name):
    #     module_args = {"command": "install", "name": pkg_name}
    #     module_return = self._execute_module(module_name="pkg_manager",
    #                                          module_args=module_args)

    #     if not module_return.get("failed"):
    #         display.display(module_return.get("msg"), color=C.COLOR_WARN)

    #     return module_return

    def _get_param_command(self):
        command = self._task.args.get("command", None)
        if command is None or command.strip() == "":
            raise StrError("Not found required param 'command'.")
        
        return command.strip()

    def _get_param_host(self, command):
        host = self._task.args.get("host", None)
        if host is None or host.strip() == "":
            raise StrError("Not found required param 'host' for command '{}'.".format(command))
        
        return host.strip()

    def _get_param_config_value(self, command):
        config = self._task.args.get("config", None)
        if config is None or config.strip() == "":
            raise StrError("Not found required param 'config' for command '{}'.".format(command))
        
        config = config.strip()
        if not os.path.exists(config):
            raise StrError("Config file '{}' not found".format(config))

        gvars = {"host": self._get_param_host(command)}
        exec(open(config).read(), gvars)
        packages = [it.strip() for it in gvars["packages"]]
        groups = [it.strip() for it in gvars["groups"]]
        return {"packages": packages, "groups": groups}

    @staticmethod
    def _print_section(text, values):
        if len(values) == 0:
            return

        display.display("{}:".format(text), color=C.COLOR_UNREACHABLE)
        for name in values:
            display.display(" {}".format(name), color=C.COLOR_VERBOSE)

    @staticmethod
    def _print_exception(text):
        display.error(text, wrap_text=False)

    def _call_module(self, name, args):
        result = self._execute_module(module_name=name, module_args=args)
        if result.get("failed"):
            exception = result.get("exception", None)
            if exception is not None:
                display.error(exception, wrap_text=False)

            raise StrError(result.get("msg", "Unknown error in module {}".format(name)))

        return result

    def _get_info(self, packages, groups):
        args = {"command": "get_info", "packages": packages, "groups": groups}
        result = self._call_module(name="pkg_manager", args=args)

        ActionModule._print_section("group, name wrong", result.get("groups_name_wrong"))
        ActionModule._print_section("package, name wrong", result.get("packages_name_wrong"))
        ActionModule._print_section("package, not installed", result.get("packages_not_installed"))
        ActionModule._print_section("package, not explicit", result.get("packages_not_explicit"))
        ActionModule._print_section("package, new", result.get("packages_new"))
        ActionModule._print_section("package, aur", result.get("packages_aur"))
        ActionModule._print_section("package, in group", result.get("packages_in_group"))
        ActionModule._print_section("package, not installed in group", result.get("packages_not_installed_in_group"))

        return result

    def _run(self):
        command = self._get_param_command()
        if command == "get_info":
            config = self._get_param_config_value(command)
            return self._get_info(config["packages"], config["groups"])
        else:
            raise StrError("Param 'command' has unexpected value '{}'.".format(command))

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)        
        try:
            result.update(self._run())
        except StrError as e:
            result['failed'] = True
            result['msg'] = "Error in action_plugin/pkg_manager" + str(e)
        except Exception:
            ActionModule._print_exception(format_exc())
            result['failed'] = True
            result['msg'] = "Error in action_plugin/pkg_manager"

        return result
