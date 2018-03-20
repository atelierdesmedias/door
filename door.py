import time, os
import pifacedigitalio
import database

open_file = open
#
# Door control library.
#
def _log(info):
    database.log_door_async(info)

def close():
    pifacedigital = pifacedigitalio.PiFaceDigital()

    pifacedigital.relays[0].turn_on()
    pifacedigital.leds[7].turn_off()

def open(source=None):
    pifacedigital = pifacedigitalio.PiFaceDigital()

    pifacedigital.leds[7].turn_on()
    pifacedigital.relays[0].turn_off()
    _log(source or "None")

def is_opened(pifacedigital):
    if pifacedigital.leds[7].value == 1:
        return True
    return False

