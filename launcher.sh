#!/bin/bash

function log() {
  time=$(date '+%Y-%m-%d %H:%M:%S')
  echo "$time, Launcher, ${1}" >> logbook.log
}

# Screen on.
export DISPLAY=:0
xset dpms force on
log "screen on"

# Python venv activate.
source ../bin/activate
log "venv activate"

# Puppet.
log "puppet start"
python -m puppet
log "puppet finished"

# Python venv deactivate.
deactivate
log "venv deactivated"

# Screen off.
xset dpms force off
log "screen off"

# Schedule next run.
at now + "$((700 + RANDOM % 60))" minutes -f ./launcher.sh
next=$(atq | awk '{print $3, $4, $5}')
log "next run $next"
