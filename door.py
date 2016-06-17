import pifacedigitalio


#
# Door control library.
#
def close():
    pifacedigital = pifacedigitalio.PiFaceDigital()

    pifacedigital.relays[0].turn_on()
    pifacedigital.leds[7].turn_off()

def open():
    pifacedigital = pifacedigitalio.PiFaceDigital()

    pifacedigital.leds[7].turn_on()
    pifacedigital.relays[0].turn_off()

def is_opened(pifacedigital):
    if pifacedigital.leds[7].value == 1:
        return True
    return False

