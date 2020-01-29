#
# Memento Pi
# Utilities for dsiplaying notification on the raspberry pi
#


import time
import threading
from gpiozero import TonalBuzzer

buzzer = TonalBuzzer(23)
# play a tone on the buzzer
def play():
    def play_fn():
        buzzer.play("A4")
        time.sleep(1)
        buzzer.stop()
    threading.Thread(target=play_fn).start()
