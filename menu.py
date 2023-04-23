# !/usr/bin/python
# Raspberry pi control
# menu to run through items
# items to display are: time, wlanIP, Eth0IP, last button called

from pyky040 import pyky040
from time import *
import time
import sys
import collections
import datetime
from subprocess import *
import RPi.GPIO as GPIO
import RPLCD



# clear screen
GPIO.cleanup()


# # Define GPIO inputs and outputs
# MODE
E_PULSE = 0.00005
E_DELAY = 0.00005
wait = 0.1


# LCD
LCD_RS = 7
LCD_E = 8
LCD_D4 = 25
LCD_D5 = 24
LCD_D6 = 23
LCD_D7 = 18

# BUTTONS
# Current
CURRENT_OPTION = 0
CURRENT_MENU = 0

# Define menu arrays
INIT = []
MAIN_MENU = ["<back>", "Play", "Settings"]
SETTINGS_MENU = ["<back>", "Volume", "AI", "MIDI"]
MENUS = [INIT, MAIN_MENU, SETTINGS_MENU]

def writeLines():


def setMenu(menu, opt):
    if(menu == 0):
        line1 = "TuneFarm"


try:
    def main():
        # Main program block
        print
        "test"

        tag = 0
        val = 0
        p = 0

        GPIO.cleanup()

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(LCD_RS, GPIO.OUT)
        GPIO.setup(LCD_E, GPIO.OUT)
        GPIO.setup(LCD_D4, GPIO.OUT)
        GPIO.setup(LCD_D5, GPIO.OUT)
        GPIO.setup(LCD_D6, GPIO.OUT)
        GPIO.setup(LCD_D7, GPIO.OUT)

        GPIO.setup(RT, GPIO.IN)
        GPIO.setup(OK, GPIO.IN)
        GPIO.setup(DN, GPIO.IN)
        GPIO.setup(RI, GPIO.IN)
        GPIO.setup(LE, GPIO.IN)
        GPIO.setup(UP, GPIO.IN)

        rt = GPIO.input(RT)
        ok = GPIO.input(OK)
        dn = GPIO.input(DN)
        ri = GPIO.input(RI)
        le = GPIO.input(LE)
        up = GPIO.input(UP)

        lcd_init()

        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("hello")

        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("press btn plz")

        p = 0
        tag = 0
        val = 0

        while True:
            # lcd_byte(LCD_LINE_2, LCD_CMD)
            rt = GPIO.input(RT)
            ok = GPIO.input(OK)
            dn = GPIO.input(DN)
            ri = GPIO.input(RI)
            le = GPIO.input(LE)
            up = GPIO.input(UP)
            if rt == False:
                # lcd_string("button = rt")
                p = "rt"
            if ok == False:
                # lcd_string("button = ok")
                p = "ok"
            if dn == False:
                # lcd_string("button = dn")
                p = "dn"
            if ri == False:
                # lcd_string("button = ri")
                p = "ri"
            if le == False:
                # lcd_string("button = le")
                p = "le"
            if up == False:
                # lcd_string("button = up")
                p = "up"
            if p != 0:
                result = message(tag, val, p)
                val = result['val']
                tag = result['tag']
                p = 0
            sleep(wait)


    def message(tag, val, button):
        lcd_byte(LCD_LINE_1, LCD_CMD)
        lcd_string("you pressed " + button)
        if button == "ok":
            tag = tag + 10
        if button == "rt":
            if tag >= 10:
                tag = tag - 10
            else:
                tag = 0
        if button == "dn":
            val = val - 1
        if button == "up":
            val = val + 1
        if button == "le":
            tag = tag - 1
        if button == "ri":
            tag = tag + 1

        lcd_byte(LCD_LINE_2, LCD_CMD)
        lcd_string("val " + str(val) + " tag " + str(tag))

        return {'tag': tag, 'val': val}


    def lcd_init():
        lcd_byte(0x33, LCD_CMD)
        lcd_byte(0x32, LCD_CMD)
        lcd_byte(0x28, LCD_CMD)
        lcd_byte(0x0C, LCD_CMD)
        lcd_byte(0x06, LCD_CMD)
        lcd_byte(0x01, LCD_CMD)


    def lcd_string(message):
        message = message.ljust(LCD_WIDTH, " ")

        for i in range(LCD_WIDTH):
            lcd_byte(ord(message[i]), LCD_CHR)


    def lcd_byte(bits, mode):

        GPIO.output(LCD_RS, mode)

        # High bits
        GPIO.output(LCD_D4, False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if bits & 0x10 == 0x10:
            GPIO.output(LCD_D4, True)
        if bits & 0x20 == 0x20:
            GPIO.output(LCD_D5, True)
        if bits & 0x40 == 0x40:
            GPIO.output(LCD_D6, True)
        if bits & 0x80 == 0x80:
            GPIO.output(LCD_D7, True)

        # Toggle 'Enable' pin
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, True)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, False)
        time.sleep(E_DELAY)

        # Low bits
        GPIO.output(LCD_D4, False)
        GPIO.output(LCD_D5, False)
        GPIO.output(LCD_D6, False)
        GPIO.output(LCD_D7, False)
        if bits & 0x01 == 0x01:
            GPIO.output(LCD_D4, True)
        if bits & 0x02 == 0x02:
            GPIO.output(LCD_D5, True)
        if bits & 0x04 == 0x04:
            GPIO.output(LCD_D6, True)
        if bits & 0x08 == 0x08:
            GPIO.output(LCD_D7, True)

        # Toggle 'Enable' pin
        time.sleep(E_DELAY)
        GPIO.output(LCD_E, True)
        time.sleep(E_PULSE)
        GPIO.output(LCD_E, False)
        time.sleep(E_DELAY)


    GPIO.cleanup()

    if __name__ == '__main__':
        main()

    GPIO.cleanup()
except Exception, e:
    GPIO.cleanup()
    print
    str(e)
