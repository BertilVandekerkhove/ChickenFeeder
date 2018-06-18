from RPi import GPIO
GPIO.setmode(GPIO.BCM)
from time import sleep
from threading import Thread

control = True

class DRV8825():

    def __init__(self, dir_pin, step_pin):
        self.step_pin = step_pin
        self.dir_pin = dir_pin
        GPIO.setup(self.step_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin, GPIO.OUT)
        GPIO.output(self.dir_pin, GPIO.LOW)

    def on(self):
        GPIO.output(self.step_pin, GPIO.HIGH)
        sleep(0.002)
        GPIO.output(self.step_pin, GPIO.LOW)
        sleep(0.002)