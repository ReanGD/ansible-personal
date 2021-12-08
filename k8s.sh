#!/bin/bash

ROOT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

cd $ROOT_DIR
/usr/bin/ansible-playbook k8s.yml --ask-become-pass --ask-vault-pass $@
