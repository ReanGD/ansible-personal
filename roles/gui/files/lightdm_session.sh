#!/bin/sh

# Run standart session wrapper
. /etc/lightdm/Xsession ""

if [ "$1" = "awesome" ] && [ -n "$HOME" ] && [ -r "$HOME/.config/start/awesome_profile.sh" ]; then
. "$HOME/.config/start/awesome_profile.sh"
fi

exec $@
