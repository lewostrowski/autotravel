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
hold=$(echo $((700 + $RANDOM % 760)))
at now + "$hold" minutes -f ./launcher.sh 

next=$(atq | awk '{print $5}')
echo "Launcher: next run scheduled at $next"
