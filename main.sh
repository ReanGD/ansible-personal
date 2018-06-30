#!/bin/bash
cd "$(dirname "$0")"
/usr/bin/ansible-playbook -i localhost, main.yml --ask-sudo-pass --ask-vault-pass --skip-tags "view_new,update" $@ $1
