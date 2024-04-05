#!/bin/bash
cd "$(dirname "$0")/.."
while ! xset q &>/dev/null; do
    sleep 1
done
export DISPLAY=:0
exec "$(dirname "$0")/run.sh"
