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


# pkg_manager: command=install name=yay
# pkg_manager: command=install name=yay, python
# pkg_manager: command=install_config config={{packages_file}}
# pkg_manager: command=get_info config={{packages_file}}
class ActionModule(ActionBase):
    TRANSFERS_FILES = False

    def _get_var_install_user(self):
        if "install_user" not in self._task_vars:
            StrError("Not install fact 'install_user'")
        result = self._task_vars["install_user"].strip()
        if result == "":
            StrError("Fact 'install_user' is empty")

        return result

    def _get_var_hostname_id(self):
        if "hostname_id" not in self._task_vars:
            StrError("Not install fact 'hostname_id'")
        result = self._task_vars["hostname_id"].strip()
        if result == "":
            StrError("Fact 'hostname_id' is empty")

        return result

    def _get_param_command(self):
        param_name = "command"
        result = self._task.args.get(param_name, "install")
        if result is None or result.strip() == "":
            raise StrError("Not found required param '{}'.".format(param_name))

        return result.strip()

    def _get_param_config_value(self, command):
        config = self._task.args.get("config", None)
        if config is None or config.strip() == "":
            raise StrError("Not found required param 'config' for command '{}'.".format(command))
        
        config = config.strip()
        if not os.path.exists(config):
            raise StrError("Config file '{}' not found".format(config))

        gvars = {"host": self._get_var_hostname_id()}
        exec(open(config).read(), gvars)
        packages = [it.strip() for it in gvars["packages"]]
        groups = [it.strip() for it in gvars["groups"]]
        return {"packages": packages, "groups": groups}

    def _get_param_name(self, command):
        param_name = "name"
        result = self._task.args.get(param_name, None)
        if result is None:
            raise StrError("Not found required param '{}' for command '{}'.".format(param_name,
                                                                                    command))

        return result

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
        install_user = self._get_var_install_user()
        orig_become = self._play_context.become
        orig_become_user = self._play_context.become_user

        if orig_become is None or orig_become is False:
            self._play_context.become = True
        if orig_become_user is None or orig_become_user != install_user:
            self._play_context.become_user = install_user

        try:
            result = self._execute_module(module_name=name, module_args=args)
            if result.get("failed"):
                exception = result.get("exception", None)
                if exception is not None:
                    display.error(exception, wrap_text=False)

                raise StrError(result.get("msg", "Unknown error in module {}".format(name)))

            return result
        finally:
            self._play_context.become = orig_become
            self._play_context.become_user = orig_become_user

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

    def _install(self, name):
        args = {"command": "install", "name": name}
        result = self._call_module(name="pkg_manager", args=args)

        return result

    def _run(self):
        command = self._get_param_command()
        if command == "get_info":
            config = self._get_param_config_value(command)
            return self._get_info(config["packages"], config["groups"])
        elif command == "install":
            name = self._get_param_name(command)
            return self._install(name)
        elif command == "install_config":
            config = self._get_param_config_value(command)
            return self._install(config["packages"])
        else:
            raise StrError("Param 'command' has unexpected value '{}'.".format(command))

    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)
        self._task_vars = task_vars
        try:
            result.update(self._run())
        except StrError as e:
            result['failed'] = True
            result['msg'] = "Error in action_plugin/pkg_manager: " + str(e)
        except Exception:
            ActionModule._print_exception(format_exc())
            result['failed'] = True
            result['msg'] = "Error in action_plugin/pkg_manager: "

        return result