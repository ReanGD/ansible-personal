#!/bin/bash
/usr/bin/ansible-playbook -i cfg/hosts archsrv.yml --ask-pass --ask-sudo-pass $@