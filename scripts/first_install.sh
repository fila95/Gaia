#!/bin/bash

scp ../scripts/install.sh pi@raspberrypi.local:install.sh

ssh -tt pi@raspberrypi.local <<'ENDSSH'
cd /var
sudo mkdir srvcs/
sudo mkdir srvcs/services/
sudo chmod 777 srvcs
sudo chmod 777 srvcs/services
exit
ENDSSH

### Copy Data
scp -rp ../services/* pi@raspberrypi.local:/var/srvcs/services
scp ../scripts/deploy.sh pi@raspberrypi.local:/var/srvcs/deploy.sh

# Setup
ssh -tt pi@raspberrypi.local <<'ENDSSH'
chmod +x install.sh
sudo ./install.sh
exit
ENDSSH
