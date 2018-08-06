#!/bin/bash
cd "$(dirname "$0")"
/usr/bin/ansible-playbook main.yml --ask-become-pass --ask-vault-pass --skip-tags "view_new,update" $@ $1
