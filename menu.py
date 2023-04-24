# !/usr/bin/python
# Raspberry pi control
# menu to run through items
# items to display are: time, wlanIP, Eth0IP, last button called

from time import *
import time
import sys
import collections
import datetime
from subprocess import *
import RPi.GPIO as GPIO
from RPLCD import CharLCD

# Current
CURRENT_OPTION = 0
CURRENT_MENU = 0

# Define menu arrays
INIT = ["TuneFarm", "<press to start>"]
MAIN_MENU = ["<back>", "Play", "Settings"]
SETTINGS_MENU = ["<back>", "Volume", "AI", "MIDI"]
MENUS = [INIT, MAIN_MENU, SETTINGS_MENU]

lcd = CharLCD(pin_rs=26,
              pin_e=19,
              pins_data=[13, 6, 5, 11],
              numbering_mode=GPIO.BCM,
              cols=16,
              rows=2,
              dotsize=8,
              auto_linebreaks=True)
lcd.cursorMode = "line"

def writeLines():
    lcd.cursor_pos = (1, 0)
    lcd.write_string('https://github.com/\n\rdbrgn/RPLCD')

def setMenu(menu, opt):
    if(menu == 0):
        curr_menu = INIT

    elif(menu == 1):
        curr_menu = MAIN_MENU

    elif(menu == 2):
        curr_menu = SETTINGS_MENU


