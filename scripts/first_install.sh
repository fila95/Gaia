#!/bin/bash

scp ../scripts/install.sh pi@raspberrypi.local:install.sh

# Setup
ssh -tt pi@raspberrypi.local <<'ENDSSH'
chmod +x install.sh
sudo ./install.sh
exit
ENDSSH
