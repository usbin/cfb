import RPi.GPIO as GPIO
import time
from hx711 import HX711
[DOUT, SCK]=[5,6]

class MeasureModule:
    def __init__(self, hx711=0):
        GPIO.setmode(GPIO.BCM)  #GPIO.BOARD:핀배열순서로 지정, GPIO.BCM:핀이름으로 지정
        self.hx711 = HX711(
            dout_pin=DOUT,
            pd_sck_pin=SCK
        )
        self.hx711.set_offset(-200000)

    def measure(self):
        w = self.hx711.get_weight_mean()
        return w/10000
