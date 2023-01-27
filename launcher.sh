#!/bin/bash

# Screen on.
export DISPLAY=:0
xset dpms force on
echo "Launcher: scren on"

# Python venv activate.
source ../bin/activate
echo "Launcher: venv activate"

# Puppet.
echo "Laucher: puppet start"
python -m puppet
echo "Laucher: puppet finished"

# Python venv deactivate.
deactivate
echo "Launcher: venv deactivate"

# Screen off.
xset dpms force off
echo "Launcher: screen off"

# Shedule next run.
hold=$(echo $((43200 + $RANDOM % 3600)))
systemd-run --on-active=$hold ./launcher.sh

echo "Launcher: next run will start in $hold seconds"
