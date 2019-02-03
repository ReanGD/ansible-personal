import os
import sys
import json
from ansible import constants as C
from ansible.plugins.action import ActionBase
from ansible.errors import AnsibleError

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


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
    def _install_pkg(self, pkg_name):
        module_args = {"command": "install", "name": pkg_name}
        module_return = self._execute_module(module_name="pkg_manager",
                                             module_args=module_args)

        if not module_return.get("failed"):
            display.display(module_return.get("msg"), color=C.COLOR_WARN)

        return module_return

    def _get_command(self):
        command = self._task.args.get("command", None)
        if command is None or command.strip() == "":
            raise AnsibleError("Not found required param 'command'.")
        
        return command.strip()

    def _get_host(self, command):
        host = self._task.args.get("host", None)
        if host is None or host.strip() == "":
            raise AnsibleError("Not found required param 'host' for command '{}'.".format(command))
        
        return host.strip()

    def _get_config_value(self, command, host):
        config = self._task.args.get("config", None)
        if config is None or config.strip() == "":
            raise AnsibleError("Not found required param 'config' for command '{}'.".format(command))
        
        config = config.strip()
        if not os.path.exists(config):
            raise AnsibleError("Config file '{}' not found".format(config))

        gvars = {"host": host}
        try:
            if sys.version_info[0] == 3:
                exec(open(config).read(), gvars)
            else:
                execfile(config, gvars)

            packages = [it.strip() for it in gvars["packages"]]
            groups = [it.strip() for it in gvars["groups"]]
            return {"packages": packages, "groups": groups}
        except:
            e = sys.exc_info()[1]
            raise AnsibleError(e)

    def _print_section(self, text, values):
        if len(values) == 0:
            return

        display.display("{}:".format(text), color=C.COLOR_UNREACHABLE)
        for name in values:
            display.display(" {}".format(name), color=C.COLOR_VERBOSE)

    def _get_info(self, packages, groups):
        module_args = {"command": "get_info", "packages": packages, "groups": groups}
        module_return = self._execute_module(module_name="pkg_manager",
                                             module_args=module_args)        
        if module_return.get("failed"):
            raise AnsibleError("Module 'pkg_manager' finished with error: {}.".format(module_return.get("msg")))

        self._print_section("group, name wrong", module_return.get("groups_name_wrong"))
        self._print_section("package, name wrong", module_return.get("packages_name_wrong"))
        self._print_section("package, not installed", module_return.get("packages_not_installed"))
        self._print_section("package, not explicit", module_return.get("packages_not_explicit"))
        self._print_section("package, new", module_return.get("packages_new"))
        self._print_section("package, aur", module_return.get("packages_aur"))
        self._print_section("package, in group", module_return.get("packages_in_group"))
        self._print_section("package, not installed in group", module_return.get("packages_not_installed_in_group"))

    def run(self, tmp=None, task_vars=None):
        result = super(ActionModule, self).run(tmp, task_vars)        
        
        command = self._get_command()            
        if command == "get_info":
            host = self._get_host(command)
            config = self._get_config_value(command, host)
            self._get_info(config["packages"], config["groups"])
            result['changed'] = False
        else:
            raise AnsibleError("Param 'command' has unexpected value '{}'.".format(command))

        return result
         # module_args['command'] = 'install'
         # module_args['name'] = "asd"
         # display.display("in params: {}".format(json.dumps(module_args)), color=C.COLOR_WARN)
         # module_return = self._install_pkg("pkg1")
         # display.display('err' if module_return.get('failed') else 'success', color=C.COLOR_WARN)

         # return module_return
