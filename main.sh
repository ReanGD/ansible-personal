#!/bin/bash
cd "$(dirname "$0")"
/usr/bin/ansible-playbook -i localhost, main.yml --ask-sudo-pass --skip-tags "view_new,update" $@
