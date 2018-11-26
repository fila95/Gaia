#!/bin/bash

cd /var/srvcs/services/definitions

for filename in *.service; do
	noext=${filename%%.*}
	sudo systemctl stop $filename
	sudo systemctl disable $filename
	sudo rm -f /lib/systemd/system/$filename
done

cd ../
sudo rm -rf definitions/*
sudo rm -rf scripts/*

# sudo systemctl daemon-reload