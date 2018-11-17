#!/bin/bash

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install gcc make build-essential python-dev git scons swig -y
sudo apt-get install python-pip
sudo apt-get install python3-pip

git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x/
sudo scons
cd python
sudo python setup.py build
sudo python setup.py install
sudo python3 setup.py build
sudo python3 setup.py install

sudo apt-get install pigpio
sudo pip3 install pigpio
sudo pip3 install asyncio
sudo systemctl enable pigpiod

cd 
sudo rm install.sh

cd
cp /boot/config.txt config.txt
sudo echo "# Enable SSH via USB" >> config.txt
sudo echo "dtoverlay=dwc2" >> config.txt
sudo echo "# Speaker Config" >> config.txt
sudo echo "dtoverlay=pwm,pin=13,func=4" >> config.txt
sudo mv config.txt /boot/config.txt