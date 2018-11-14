#!/bin/bash

cd /var/srvcs/services/definitions

for filename in *.service; do
	noext=${filename%%.*}
	sudo systemctl stop $filename
	sudo rm /lib/systemd/system/$filename
done

cd ../
sudo rm -rf definitions/*
sudo rm -rf scripts/*

systemctl daemon-reload