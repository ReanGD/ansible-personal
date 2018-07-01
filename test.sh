#!/bin/bash
cd "$(dirname "$0")"
/usr/bin/ansible-playbook -i localhost, main.yml --ask-become-pass --ask-vault-pass --tags "test,init" $@ $1
