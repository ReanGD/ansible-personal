#!/bin/bash	

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cd $ROOT_DIR
/usr/bin/ansible-playbook tasks/common/main_root.yml --ask-become-pass --skip-tags "view_new,update" $@
