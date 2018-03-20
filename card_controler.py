import evdev
import database
import door
import time

#
# Service to read the card reader (RFID)
# and open (or not) the door based on what's in the DB
#
device = evdev.InputDevice('/dev/input/event0')

cardcode = ''
for event in device.read_loop():
    if event.type == evdev.ecodes.EV_KEY:
        keyevent = evdev.categorize(event)
        if keyevent.keystate == 1:
            code = int(keyevent.scancode)
            if code == 28:
                success = False
                if database.containsCard(cardcode):
                   door.open(cardcode)
                   time.sleep(3)
                   door.close()
                   success = True
                database.log_card(cardcode, success)
                cardcode = ''
            elif code == 11:
                cardcode = cardcode + '0'
            else:
                cardcode = cardcode + str(code - 1)
