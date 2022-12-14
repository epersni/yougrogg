#!/usr/bin/python3

import RPi.GPIO as GPIO
import time

#relay1 = 29 #works
#relay1 = 31 #works
#relay1 = 33 #works
#relay1 = 35 #work
#relay1 = 37 #work
#relay1 = 40 #work
#relay1 = 38 #work
#relay1 = 36 #work


GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay1, GPIO.OUT)

GPIO.output(relay1, GPIO.HIGH)
time.sleep(2)
GPIO.output(relay1, GPIO.LOW)
time.sleep(2)

GPIO.cleanup()


