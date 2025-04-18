                                
#!/usr/bin/env python3

from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO

reader = SimpleMFRC522()

try:
    print("Hold a tag near the reader...")
    id, text = reader.read()
    print("Tag UID:", id)
    print("Tag text:", text.strip())
finally:
    GPIO.cleanup()

