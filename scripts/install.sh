#!/bin/bash

sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install gcc make build-essential python-dev git scons swig -y
git clone https://github.com/jgarff/rpi_ws281x
cd rpi_ws281x/
sudo scons
cd python
sudo python setup.py build
sudo python setup.py install

sudo apt-get install python-pip
sudo apt-get install python3-pip

sudo apt-get install pigpio

# sudo pip install pigpio
sudo pip3 install pigpio

# sudo pip install asyncio
sudo pip3 install asyncio

# sudo pip install adafruit-ws2801
# sudo pip3 install adafruit-ws2801

cd 
sudo rm install.sh

sudo cat << EOF >> /boot/config.txt

# Enable SSH via USB
dtoverlay=dwc2

# Speaker Config
dtoverlay=pwm,pin=13,func=4

EOF