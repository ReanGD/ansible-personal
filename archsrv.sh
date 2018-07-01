#!/bin/bash
cd "$(dirname "$0")"
/usr/bin/ansible-playbook archsrv.yml --ask-pass --ask-become-pass $@ $1