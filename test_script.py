from time import sleep
import RPi.GPIO as GPIO
import time

# Tester code to check if GPIO pins could be used in a python script run from Go
# Used to make sure this was a viable solution before writing the whole menu out!
# This is the LED blink code from class (CS121).
def main():
    PIN = 15

    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(PIN, GPIO.OUT)

    print("LED On")
    GPIO.output(PIN, GPIO.HIGH)

    # One second pause for LED on
    time.sleep(1)
    print("LED Off")
    GPIO.output(PIN, GPIO.LOW)


if __name__ == "__main__":
    main()


