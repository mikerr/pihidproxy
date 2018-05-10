# pihidproxy
Bridge Bluetooth keyboard and mouse to USB (hid proxy)

![Imgur](https://i.imgur.com/cpGkjXw.png)

If you have a bluetooth keyboard, you can't access BIOS or OS without a BT stack.
This project acts as a bridge so the PC only sees a USB keyboard and so works without drivers.
It works by copying keypresses from the bluetooth keyboard to the piZero's USB.

Requirements:

Raspberry Pi Zero
Bluetooth keyboard

Initial setup:

    echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
    echo "dwc2" | sudo tee -a /etc/modules
    echo "libcomposite" | sudo tee -a /etc/modules

put the following in /etc/rc.local

    pair.sh
    setuphid.sh
    keys.py

pair.sh - bash script to pair & connect bluetooth on boot.

setuphid.sh - installs the USB keybaord driver

keys.py - reads keyboard (e.g. bluetooth) and translates keycodes, then sends it over USB.


