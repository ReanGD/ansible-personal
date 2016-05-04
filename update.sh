#!/bin/bash
/usr/bin/ansible-playbook -i localhost, main.yml --ask-sudo-pass --tags "update" $@
