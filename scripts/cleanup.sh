#!/bin/bash

FOLDER=/var/srvcs/services/definitions

if [ -d $FOLDER ]
then
	cd $FOLDER

	for filename in *.service; do
		noext=${filename%%.*}
		sudo systemctl stop $filename
		sudo systemctl disable $filename
		sudo rm -f /lib/systemd/system/$filename
	done

	cd ../
	sudo rm -rf definitions/*
	sudo rm -rf scripts/*

fi

# sudo systemctl daemon-reload