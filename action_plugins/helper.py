from ansible.module_utils.basic import AnsibleModule


class AnsibleModuleWrapper(AnsibleModule):
    def __init__(self, base, run_command_environ_update):
        self.base = base
        self.run_command_environ_update = run_command_environ_update
        self.no_log_values = set()
        self._debug = False

    def log(self, msg, log_args=None):
        pass

    def fail_json(self, **kwargs):
        self.add_path_info(kwargs)
        if 'msg' not in kwargs:
            self.base.exit_failed('mplementation error -- msg to explain the error is required')
        else:
            self.base.exit_failed(kwargs['msg'])


class ExitException(Exception):
    pass


class BaseActionModule(object):
    def base_run(self, cls, task_vars, required_params):
        self.run_command_environ_update = {}
        if task_vars is None:
            task_vars = dict()
        self._result = super(cls, self).run(None, task_vars)

        try:
            params = {}
            for name in required_params:
                if name in self._task.args:
                    params[name] = self._task.args.get(name)
                else:
                    self.exit_failed('Not found param \'%s\'' % name)
            self.impl(**params)
        except ExitException:
            pass
        except Exception:
            raise
        return self._result

    def exit(self):
        raise ExitException()

    def exit_changed(self):
        self._result['changed'] = True
        raise ExitException()

    def exit_failed(self, msg):
        self._result['failed'] = True
        self._result['msg'] = msg
        raise ExitException()

    def get_bin_path(self, arg, required=False, opt_dirs=[]):
        wrapper = AnsibleModuleWrapper(self, self.run_command_environ_update)
        return wrapper.get_bin_path(arg, required, opt_dirs)

    def run_command(self, args, check_rc=False, close_fds=True, executable=None, data=None, binary_data=False, path_prefix=None, cwd=None, use_unsafe_shell=False, prompt_regex=None, environ_update=None):
        wrapper = AnsibleModuleWrapper(self, self.run_command_environ_update)
        return wrapper.run_command(args, check_rc, close_fds, executable, data, binary_data, path_prefix, cwd, use_unsafe_shell, prompt_regex, environ_update)
