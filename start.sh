#!/bin/bash

#
# Script called by /etc/init.d
#
cd /usr/local/door

python3 init.py
python3 door_button_controller.py &
python3 card_controler.py &

sleep 3

echo "Close the door"
python3 close.py
