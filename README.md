# pihidproxy
Bridge Bluetooth keyboard and mouse to USB (hid proxy)

Initial setup:

    echo "dtoverlay=dwc2" | sudo tee -a /boot/config.txt
    echo "dwc2" | sudo tee -a /etc/modules
    echo "libcomposite" | sudo tee -a /etc/modules

put the following in /etc/rc.local

    pair.sh
    setuphid.sh
    keys.py

