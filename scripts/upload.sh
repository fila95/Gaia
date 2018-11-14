#!/bin/bash

# Setup
ssh -tt pi@raspberrypi.local <<'ENDSSH'
cd /var
sudo mkdir srvcs/
sudo mkdir srvcs/services/
sudo chmod 777 srvcs
sudo chmod 777 srvcs/services
exit
ENDSSH

# Clean Previous
scp ../scripts/cleanup.sh pi@raspberrypi.local:/var/srvcs/cleanup.sh
ssh -tt pi@raspberrypi.local <<'ENDSSH'
cd /var/srvcs/
./cleanup.sh
exit
ENDSSH


### Copy Data
scp -rp ../services/* pi@raspberrypi.local:/var/srvcs/services
scp ../scripts/deploy.sh pi@raspberrypi.local:/var/srvcs/deploy.sh

# Start
ssh -tt pi@raspberrypi.local <<'ENDSSH'
cd /var/srvcs/
sudo ./deploy.sh
exit
ENDSSH