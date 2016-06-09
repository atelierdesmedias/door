import pifacedigitalio

#
# called by /etc/init.d to put the door in the right state,
# i.e. initialize the relay, the switch and the LED card
#
pifacedigitalio.init()
