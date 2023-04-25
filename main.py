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
    from RPLCD import CharLCD

logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG if os.getenv('DEBUG', '') == 'True' else logging.INFO)

CLK_PIN = 17
DT_PIN = 18
SW_PIN = 27

lcd = CharLCD(pin_rs=26,
              pin_e=19,
              pins_data=[13, 6, 5, 11],
              numbering_mode=GPIO.BCM,
              cols=16,
              rows=2,
              dotsize=8,
              auto_linebreaks=True)

INIT_0_MENU = ["Main", "<press for menu>"]
MAIN_1_MENU = ["<back>", "Play", "Settings"]
SETTINGS_2_MENU = ["<back>", "Volume", "AI", "MIDI"]
MENUS = [INIT_0_MENU, MAIN_1_MENU, SETTINGS_2_MENU]
MENU_LEVEL = 0
OPTION = 0
CURR_MENU = INIT_0_MENU


def change(count):
    global OPTION, CURR_MENU, MENU_LEVEL
    logger.info(count)
    OPTION = count
    logger.info("Menu Level:" + str(MENU_LEVEL) + ", Option: " + str(OPTION))
    if (MENU_LEVEL == 0):
        lcd.clear()
        lcd.write_string(CURR_MENU[0] + "\n\r" + CURR_MENU[1])
    elif (OPTION < (len(CURR_MENU) - 1)):
        lcd.clear()
        lcd.write_string("* " + CURR_MENU[OPTION] + "\n\r  " + CURR_MENU[OPTION + 1])
    else:
        lcd.clear()
        lcd.write_string("  " + CURR_MENU[OPTION - 1] + "\n\r" + "* " + CURR_MENU[OPTION])


def select():
    global encoder, OPTION, MENU_LEVEL, CURR_MENU

    # log info about condition of menu
    logger.info("Selection occurred")
    logger.info("Menu Level:" + str(MENU_LEVEL) + ", Option: " + str(OPTION))

    # handle back button
    if (MENU_LEVEL > 0 and OPTION == 0):
        MENU_LEVEL -= 1
    else:
        MENU_LEVEL += 1

    # reset option to 0
    OPTION = 0

    # set current menu value
    CURR_MENU = MENUS[MENU_LEVEL]

    # handle main menu
    if (MENU_LEVEL == 0):
        encoder.setup(scale_min=0, scale_max=(len(MENUS[MENU_LEVEL]) - 1))
        lcd.clear()
        lcd.write_string(CURR_MENU[0] + "\n\r" + CURR_MENU[1])
    # handle volume menu
    elif (MENU_LEVEL == 10):    # change this value
        encoder.setup(scale_min=0, scale_max=100)
        lcd.clear()
        lcd.write_string("* " + CURR_MENU[OPTION] + "\n\r  " + CURR_MENU[OPTION + 1])
    # handle normal menu stuff
    else:
        encoder.setup(scale_min=0, scale_max=(len(MENUS[MENU_LEVEL]) - 1))
        lcd.clear()
        lcd.write_string("* " + CURR_MENU[OPTION] + "\n\r  " + CURR_MENU[OPTION + 1])


def inc_global_volume(count):
    logger.info("Incrementing global volume")
    # Using Popoen for async (we do not want to perturbate the audio)
    subprocess.Popen(["pactl", "set-sink-volume", "0", "+" + str(VOLUME_STEP) + "%"])


def dec_global_volume(count):
    logger.info("Decrementing global volume")
    subprocess.Popen(["pactl", "set-sink-volume", "0", "-" + str(VOLUME_STEP) + "%"])


try:
    lcd.cursorMode = "hide"
    lcd.write_string(CURR_MENU[0] + "\n\r" + CURR_MENU[1])
    lcd.cursor_pos = (0, 0)

    if has_gpio:
        encoder = pyky040.Encoder(CLK=CLK_PIN, DT=DT_PIN, SW=SW_PIN)
        encoder.setup(scale_min=0, scale_max=1, step=1, chg_callback=change, sw_callback=select)
        encoder_thread = threading.Thread(target=encoder.watch)

        encoder_thread.start()

    # Do other stuff
    print('Other stuff...')
    while True:
        sleep(1000)


except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
   print("Keyboard interrupt")

except:
   print("Error")

finally:
   print("clean up")
   GPIO.cleanup() # cleanup all GPIO
