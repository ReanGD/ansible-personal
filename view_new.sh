#!/bin/bash
cd "$(dirname "$0")"
/usr/bin/ansible-playbook -i localhost, main.yml --tags "view_new" $@
