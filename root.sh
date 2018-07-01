#!/bin/bash
cd "$(dirname "$0")"
/usr/bin/ansible-playbook -i localhost, root.yml --ask-become-pass --skip-tags "view_new,update" $@ $1
