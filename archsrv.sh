#!/bin/bash
cd "$(dirname "$0")"
/usr/bin/ansible-playbook archsrv.yml --ask-pass --ask-sudo-pass $@ $1