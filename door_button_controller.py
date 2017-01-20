import door
import time
import pifacedigitalio

pfd = pifacedigitalio.PiFaceDigital()

while True:
    if pfd.input_pins[4].value == 1:
        door.open("Button")
        time.sleep(3)
        door.close()

    # Just to be nice with the proc
    time.sleep(0.1)
