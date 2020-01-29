import re
import time
import argparse
import luma.core
import luma.led_matrix
import gpiozero

#import max7219.led as led 

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT
from gpiozero import Button
from gpiozero import LED
from time import sleep

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=4, block_orientation=-90)
#device = led.matrix(serial, cascaded=4, block_orientation=-90)
# x = 0
# msg = "Your late hoe"
# msg = "Deadline ebwf"

def displaymsg():
    x=0
    for a in range (7):



        #states where theZ
        if(x == 0):
            msg = "Your task is due now"
        elif (x == 1):
            msg = "Your task is due now"
        elif (x == 2):
            msg = "Your task is due now"

        show_message(device, msg, fill="white", font=proportional(LCD_FONT),scroll_delay=0.025)
        time.sleep(0.05)
        x += 1
        if(x > 2):
            x = 0

