#!/usr/bin/env python3

from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

try:
    text = input("Enter text to write: ")
    print("Now place your tag near the reader...")
    reader.write(text)
    print("Written!")
finally:
    GPIO.cleanup()





