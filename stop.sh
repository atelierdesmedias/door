#
# Script called by /etc/init.d (only for 'init.d restart')
#
echo 'Stopping...'
pkill -f 'python3 door_button_controller.py'
pkill -f 'python3 card_controler.py'
python3 /usr/local/door/open.py

exit 0
