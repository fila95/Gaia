#!/bin/bash

# cd ../services/definitions
cd /var/srvcs/services/definitions

for filename in *.service; do
	noext=${filename%%.*}
	echo $noext

	sudo cp $filename /lib/systemd/system/$filename
	sudo chmod 644 /lib/systemd/system/$filename

	sudo systemctl start $filename
	# sudo systemctl status $filename
done

systemctl daemon-reload