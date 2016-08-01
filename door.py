import time, os
import pifacedigitalio

open_file = open
#
# Door control library.
#
def _log(info):
    LOGFILE='/tmp/opened.log'
    if os.path.exists(LOGFILE) and (os.path.getsize(LOGFILE) > (100 * 1000 * 1000)):
        os.remove(LOGFILE)
    with open_file(LOGFILE, 'a') as file:
        file.write(time.strftime("%Y-%m-%d %H:%M:%S ") + info + "\n")
    
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

