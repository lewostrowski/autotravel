#!/bin/bash

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
