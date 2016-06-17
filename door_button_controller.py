import door
import time
import pifacedigitalio
import threading 

#
# Switch to open/close the door (in french "bouton"... thus "button")
#
pfd = pifacedigitalio.PiFaceDigital()

def threadLoop():
    time.sleep(3)
    door.close()

def press(event):
    if not door.is_opened(pfd):
        door.open()
        threading.Thread(target=threadLoop).start()

listener = pifacedigitalio.InputEventListener()
listener.register(4, pifacedigitalio.IODIR_FALLING_EDGE, press)
listener.activate()
