#!/bin/bash	

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cd $ROOT_DIR
/usr/bin/ansible-playbook tasks/common/main_user_pc.yml --ask-become-pass --ask-vault-pass --skip-tags "view_new,update" $@
