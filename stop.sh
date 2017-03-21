#
# Script called by /etc/init.d (only for 'init.d restart')
#
kill $(ps auwwx | grep 'door_button_controller.py' | awk '{print $2}')
kill $(ps auwwx | grep 'card_controler.py' | awk '{print $2}')
kill $(ps auwwx | grep 'monitoring.py' | awk '{print $2}')
python3 /usr/local/door/open.py

exit 0
