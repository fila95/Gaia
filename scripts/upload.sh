#!/bin/bash

###
ssh -tt pi@raspberrypi.local <<'ENDSSH'
cd /var
sudo mkdir srvcs/
sudo chmod 777 srvcs
exit
ENDSSH

### Copy Data
scp -rp ../services/* pi@raspberrypi.local:/var/srvcs
scp ../scripts/deploy.sh pi@raspberrypi.local:/var/srvcs/deploy.sh

###
ssh -tt pi@raspberrypi.local <<'ENDSSH'
cd /var/srvcs/
sudo ./deploy.sh
exit
ENDSSH