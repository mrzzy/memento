#
# Memento Pi
# Utilities for dsiplaying notification on the raspberry pi
#

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

# setup led display
led_serial = spi(port=0, device=0, gpio=noop())
led_display = max7219(led_serial, cascaded=4, block_orientation=-90)


# show the given message on the led display
# msg - message to show  on the display
def show(msg):
    show_message(led_display, msg, fill="white", font=proportional(LCD_FONT),scroll_delay=0.025)
