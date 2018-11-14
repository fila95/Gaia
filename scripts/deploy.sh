#!/bin/bash

# cd ../services/definitions
cd /var/srvcs/services/definitions

for filename in *.service; do
	noext=${filename%%.*}

	sudo cp $filename /lib/systemd/system/$filename
	sudo chmod 644 /lib/systemd/system/$filename

	sudo systemctl start $filename
	sudo systemctl enable $filename
	# sudo systemctl status $filename
done

systemctl daemon-reload