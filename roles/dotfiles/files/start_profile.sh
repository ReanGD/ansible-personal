#!/bin/sh

if [ -n "$HOME" ] && [ -r "$HOME/.config/start/login_profile.sh" ]; then
. "$HOME/.config/start/login_profile.sh"
fi
