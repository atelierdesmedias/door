#!/bin/bash

# Retart MySQL server just in case
/etc/init.d/mysql restart

#
# Script called by /etc/init.d
#
cd /usr/local/door

python3 init.py
python3 door_button_controller.py &
python3 card_controler.py &
python3 monitoring.py &

sleep 3

echo "Close the door"
python3 close.py

exit 0
