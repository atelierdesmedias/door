#
# Script called by /etc/init.d (only for 'init.d restart')
#
kill $(ps auwwx | grep '[p]ython3 door_button_controller.py' | awk '{print $2}')
kill $(ps auwwx | grep '[p]ython3 card_controler.py' | awk '{print $2}')
kill $(ps auwwx | grep '[p]ython3 monitoring.py' | awk '{print $2}')
python3 /usr/local/door/open.py
