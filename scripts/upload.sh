#!/bin/bash

# Setup
ssh -tt pi@gaia2.local <<'ENDSSH'
cd /var
sudo mkdir srvcs/
sudo mkdir srvcs/services/
sudo chmod 777 srvcs
sudo chmod 777 srvcs/services
exit
ENDSSH

# Clean Previous
scp ../scripts/cleanup.sh pi@gaia2.local:/var/srvcs/cleanup.sh
ssh -tt pi@gaia2.local <<'ENDSSH'
cd /var/srvcs/
sudo chmod 777 cleanup.sh
sudo ./cleanup.sh
exit
ENDSSH


### Copy Data
scp -rp ../services/* pi@gaia2.local:/var/srvcs/services
scp ../scripts/deploy.sh pi@gaia2.local:/var/srvcs/deploy.sh

# Start
ssh -tt pi@gaia2.local <<'ENDSSH'
cd /var/srvcs/
sudo chmod 777 services/*
sudo ./deploy.sh
exit
ENDSSH