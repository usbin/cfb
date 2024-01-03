# Based on: https://www.raspberrypi.org/forums/viewtopic.php?t=242928\.
#
# Software to drive 4 wire stepper motor using a TB6600 Driver
# PRi - RPi 3B
#
# Route 3.3 VDC to the controller "+" input for each: ENA_A, PUL_A, and DIR_A
#
# Connect GPIO pins as shown below) to the "-" input for each: ENA_A, PUL_A, and DIR_A
#
#
from time import sleep
import RPi.GPIO as GPIO
#
PUL_A = 17  # Stepper Drive Pul_Ases
DIR_A = 27  # Controller Direction Bit (High for Controller default / LOW to Force a Direction Change).
ENA_A = 22  # Controller Enable Bit (High to Enable / LOW to Disable).
DIR_B = 14
PUL_B = 15
ENA_B = 18
# DIRI = 14  # Status Indicator LED - Direction
# ENAI = 15  # Status indicator LED - Controller Enable
#
# NOTE: Leave DIR_A and ENA_A disconnected, and the controller WILL drive the motor in Default direction if PUL_A is applied.
#
GPIO.setmode(GPIO.BCM)
# GPIO.setmode(GPIO.BOARD) # Do NOT use GPIO.BOARD mode. Here for comparison only.
#
GPIO.setup(PUL_A, GPIO.OUT)
GPIO.setup(DIR_A, GPIO.OUT)
GPIO.setup(ENA_A, GPIO.OUT)
GPIO.setup(PUL_B, GPIO.OUT)
GPIO.setup(DIR_B, GPIO.OUT)
GPIO.setup(ENA_B, GPIO.OUT)
# GPIO.setup(DIRI, GPIO.OUT)
# GPIO.setup(ENAI, GPIO.OUT)
#
# print('PUL_A = GPIO 17 - RPi 3B-Pin #11')
# print('DIR_A = GPIO 27 - RPi 3B-Pin #13')
# print('ENA_A = GPIO 22 - RPi 3B-Pin #15')
# print('ENAI = GPIO 14 - RPi 3B-Pin #8')
# print('DIRI = GPIO 15 - RPi 3B-Pin #10')

#
print('Initialization Completed')
#
# Could have usesd only one DURATION constant but chose two. This gives play options.
durationFwd = 7920 # This is the duration of the motor spinning. used for forward direction
durationBwd = 7920 # This is the duration of the motor spinning. used for reverse direction
print('Duration Fwd set to ' + str(durationFwd))
print('Duration Bwd set to ' + str(durationBwd))
#
delay = 0.00005
 # This is actualy a delay between PUL_A pul_Ases - effectively sets the mtor rotation speed.
print('Speed set to ' + str(delay))
#
cycles = 1 # This is the number of cycles to be run once program is started.
cyclecount = 0 # This is the iteration of cycles to be run once program is started.
print('number of Cycles to Run set to ' + str(cycles))
#
#
def forward():
    GPIO.output(ENA_A, GPIO.HIGH)
    GPIO.output(ENA_B, GPIO.HIGH)
    print('ENA_A set to HIGH - Controller Enabled')
    #
    sleep(.5) # pause due to a possible change direction
    GPIO.output(DIR_A, GPIO.LOW)
    GPIO.output(DIR_B, GPIO.LOW)
    print('DIR_A set to LOW - Moving Forward at ' + str(delay))
    print('Controller PUL_A being driven.')
    for x in range(durationFwd):
        GPIO.output(PUL_A, GPIO.HIGH)
        GPIO.output(PUL_B, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL_A, GPIO.LOW)
        GPIO.output(PUL_B, GPIO.LOW)
        sleep(delay)
    GPIO.output(ENA_A, GPIO.LOW)
    print('ENA_A set to LOW - Controller Disabled')
    sleep(.5) # pause for possible change direction
    return
#
#
def reverse():
    GPIO.output(ENA_A, GPIO.HIGH)
    GPIO.output(ENA_B, GPIO.HIGH)
    print('ENA_A set to HIGH - Controller Enabled')
    #
    sleep(.5) # pause due to a possible change direction
    GPIO.output(DIR_A, GPIO.HIGH)
    GPIO.output(DIR_B, GPIO.HIGH)
    print('DIR_A set to HIGH - Moving Backward at ' + str(delay))
    print('Controller PUL_A being driven.')
    #
    for y in range(durationBwd):
        GPIO.output(PUL_A, GPIO.HIGH)
        GPIO.output(PUL_B, GPIO.HIGH)
        sleep(delay)
        GPIO.output(PUL_A, GPIO.LOW)
        GPIO.output(PUL_B, GPIO.LOW)
        sleep(delay)
    GPIO.output(ENA_A, GPIO.LOW)
    GPIO.output(ENA_B, GPIO.LOW)
    print('ENA_A set to LOW - Controller Disabled')
    sleep(.5) # pause for possible change direction
    return

while cyclecount < cycles:
    forward()
    reverse()
    #reverse()
    cyclecount = (cyclecount + 1)
    print('Number of cycles completed: ' + str(cyclecount))
    print('Number of cycles remaining: ' + str(cycles - cyclecount))
#
GPIO.cleanup()
print('Cycling Completed')
#
