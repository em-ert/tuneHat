# Import the module and threading
import threading
import logging
import subprocess
from time import sleep
import os

try:
    from RPi import GPIO
    has_gpio = True
except ImportError:
    has_gpio = False

if has_gpio:
    from pyky040 import pyky040

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG if os.getenv('DEBUG', '') == 'True' else logging.INFO)

CLK_PIN = 17
DT_PIN = 18
SW_PIN = 27


INIT_0_MENU = ["Main", "Press for menu"]
MAIN_1_MENU = ["<back>", "Play", "Settings"]
SETTINGS_2_MENU = ["<back>", "Volume", "AI", "MIDI"]
MENUS = [INIT_0_MENU, MAIN_1_MENU, SETTINGS_2_MENU]
MENU_LEVEL = 0
OPTION = 0

def increment(count):
    global MENU_LEVEL
    logger.info(count)


def decrement(count):
    global MENU_LEVEL
    logger.info(count)
    if(MENU_LEVEL >= 0 and MENU_LEVEL <= 3):
        MENU_LEVEL += 1

def select():
    logger.info("Selection occured")
    global encoder
    encoder.setup(scale_min=0, scale_max=10)

def inc_global_volume(count):
    logger.info("Incrementing global volume")
    # Using Popoen for async (we do not want to perturbate the audio)
    subprocess.Popen(["pactl", "set-sink-volume", "0", "+" + str(VOLUME_STEP) + "%"])

def dec_global_volume(count):
    logger.info("Decrementing global volume")
    subprocess.Popen(["pactl", "set-sink-volume", "0", "-" + str(VOLUME_STEP) + "%"])


encoder = pyky040.Encoder(CLK=CLK_PIN, DT=DT_PIN, SW=SW_PIN)
encoder.setup(scale_min=0, scale_max=5, step=1, inc_callback=increment, dec_callback=decrement, sw_callback=select)
encoder_thread = threading.Thread(target=encoder.watch)

encoder_thread.start()

# Do other stuff
print('Other stuff...')
while True:
    sleep(1000)