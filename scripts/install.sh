#!/bin/bash

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install gcc make build-essential python-dev git scons swig -y
sudo apt-get install python-pip -y
sudo apt-get install python3-pip -y
sudo apt-get install python3-dev python3-numpy -y

sudo apt-get install python3-pygame -y
sudo pip3 install pygame

git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x/
sudo scons
cd python
sudo python setup.py build
sudo python setup.py install
sudo python3 setup.py build
sudo python3 setup.py install

sudo apt-get install pigpio -y
sudo pip3 install pigpio
sudo systemctl enable pigpiod

sudo pip3 install asyncio

cd 
# sudo rm install.sh

# cd
# cp /boot/config.txt config.txt
# sudo echo "# Enable SSH via USB" >> config.txt
# sudo echo "dtoverlay=dwc2" >> config.txt
# sudo echo "# Speaker Config" >> config.txt
# sudo echo "dtoverlay=pwm,pin=19,func=4" >> config.txt
# sudo mv config.txt /boot/config.txt

# sudo sed '$ s/$/rootwait/ modules-load=dwc2,g_ether' /boot/cmdline.txt

# cd
# sudo awk '{gsub(/rootwait/,"rootwait modules-load=dwc2,g_ether")}1' /boot/cmdline.txt > cmdline.txt
# sudo mv cmdline.txt /boot/cmdline.txt

sudo reboot