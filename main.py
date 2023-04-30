# Import the module and threading
import threading
import logging
import subprocess
from time import sleep
import os
import alsaaudio

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

#
MENU_LEVEL = 0
OPTION = 0
VOLUME = 0
SUBMENU = False

# Menu arrays
INIT_0_MENU = ["Main", "<press for menu>"]
MAIN_1_MENU = ["<back>", "Play", "Settings"]
SETTINGS_2_MENU = ["<back>", "AI", "Volume", "MIDI"]
AI_3_MENU = ["<back>", "AI", "Volume", "MIDI"]
VOLUME_4_MENU = [VOLUME]
MIDI_5_MENU = [""]

# Main Menu array and current menu variable
MENUS = [INIT_0_MENU, MAIN_1_MENU, SETTINGS_2_MENU, AI_3_MENU, VOLUME_4_MENU, MIDI_5_MENU]
CURR_MENU = INIT_0_MENU


def change(count):
    global OPTION, CURR_MENU, MENU_LEVEL, VOLUME
    logger.info(count)
    if (OPTION == count):
        return
    OPTION = count
    logger.info("Menu Level:" + str(MENU_LEVEL) + ", Option: " + str(OPTION))

    # Handle submenus (2-6)
    if (MENU_LEVEL == 4):
        lcd.clear()
        lcd.write_string(str(OPTION))
    elif (MENU_LEVEL == 0):
        pass
    elif (OPTION < (len(CURR_MENU) - 1)):
        lcd.clear()
        lcd.write_string("* " + CURR_MENU[OPTION] + "\n\r  " + CURR_MENU[OPTION + 1])
    else:
        lcd.clear()
        lcd.write_string("  " + CURR_MENU[OPTION - 1] + "\n\r" + "* " + CURR_MENU[OPTION])


def select():
    global encoder, OPTION, MENU_LEVEL, CURR_MENU, VOLUME, SUBMENU

    # log info about condition of menu
    logger.info("Selection occurred")
    logger.info("Menu Level:" + str(MENU_LEVEL) + ", Option: " + str(OPTION))

    # handle back button for levels 2 and under
    if (MENU_LEVEL > 0 and MENU_LEVEL <= 2 and OPTION == 0):
        MENU_LEVEL -= 1
    # handle submenus
    elif (MENU_LEVEL == 2 and OPTION != 0):
        # Offset menu levels to account for the options
        MENU_LEVEL = 2 + OPTION
        SUBMENU = True
    # handle exit from volume menu
    elif (MENU_LEVEL == 4):
        mixer.setvolume(OPTION)
        MENU_LEVEL = 2
        SUBMENU = False
    else:
        MENU_LEVEL += 1

    # reset option to 0
    OPTION = 0
    # set current menu value
    CURR_MENU = MENUS[MENU_LEVEL]

    # handle initialization menu
    if MENU_LEVEL == 0:
        encoder.setup(scale_min=0, scale_max=1)
        lcd.clear()
        lcd.write_string(INIT_0_MENU[0] + "\n\r" + INIT_0_MENU[1])

    # handle initialization of volume menu
    elif MENU_LEVEL == 4:    # for volume
        m = mixer.getvolume()
        VOLUME = m[0]
        encoder.setup(scale_min=0, scale_max=100)
        encoder.counter = VOLUME
        lcd.clear()
        lcd.write_string(str(VOLUME))

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
        mixer = alsaaudio.Mixer()
        m = mixer.getvolume()
        VOLUME = m[0]
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
