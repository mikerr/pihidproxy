#!/bin/bash
devicename="NexDock"

echo "Finding BT device *$devicename* ..."
scan=$(sudo hcitool scan)
found=$(grep $devicename <<< $scan)
if [ $? -eq 0 ]
then
        mac=$(cut -f 2 <<< $found)
        echo $mac
        echo "
agent on
scan on
pair $mac
connect $mac" | sudo bluetoothctl


else
        echo not found
fi
