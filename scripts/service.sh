#!/bin/bash
export DISPLAY=:0
while ! xset q &>/dev/null; do
    sleep 1
done
exec "$(dirname "$0")/run.sh"
