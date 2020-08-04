#!/bin/sh

# Run standart session wrapper
. /etc/lightdm/Xsession

if [ -n "$HOME" ] && [ -r "$HOME/.config/start/startx_profile.sh" ]; then
. "$HOME/.config/start/startx_profile.sh"
fi

exec $@
