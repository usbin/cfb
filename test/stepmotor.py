import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)  #GPIO.BOARD:핀배열순서로 지정, GPIO.BCM:핀이름으로 지정
[EN, DIR, PUL]=[22, 27, 17]
DELAY = 0.0001

# Setup
GPIO.setup([EN, DIR, PUL], GPIO.OUT)

try:
    while True:
        GPIO.output(EN, GPIO.HIGH)
        GPIO.output(DIR, GPIO.LOW)
        GPIO.output(PUL, GPIO.LOW)
        time.sleep(DELAY)
        GPIO.output(PUL, GPIO.HIGH)
        time.sleep(DELAY)
finally:
    GPIO.cleanup()


# import RPi.GPIO as GPIO
# import time

# GPIO.setmode(GPIO.BCM)  #GPIO.BOARD:핀배열순서로 지정, GPIO.BCM:핀이름으로 지정
# [EN, DIR, PUL]=[22, 27, 17]
# DELAY = 0.00001

# # Setup
# GPIO.setup([EN, DIR, PUL], GPIO.OUT)

# try:
#     while True:
#         GPIO.output(EN, GPIO.HIGH)
#         GPIO.output(DIR, GPIO.LOW)
#         #GPIO.output(PUL, GPIO.HIGH)
#         GPIO.output(PUL, GPIO.LOW)
#         time.sleep(DELAY)
#         GPIO.output(PUL, GPIO.HIGH)

#         time.sleep(0.5)


#         GPIO.output(EN, GPIO.HIGH)
#         GPIO.output(DIR, GPIO.HIGH)
#         time.sleep(DELAY)
#         GPIO.output(PUL, GPIO.LOW)
#         time.sleep(DELAY)
#         GPIO.output(PUL, GPIO.HIGH)
#         time.sleep(0.5)
# finally:
#     GPIO.cleanup()