#!/bin/bash	

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cd $ROOT_DIR
/usr/bin/ansible-playbook local_install.yml --ask-become-pass $@