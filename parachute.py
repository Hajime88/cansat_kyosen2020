import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
#今は適当に決めてる
heat_pin = 29
GPIO.setup(heat_pin, GPIO.OUT, initial = GPIO.LOW)

#パラシュート分離
def parachute_sep():
    GPIO.output(heat_pin,GPIO.HIGH)
    time.sleep(2.0)
    GPIO.output(heat_pin,GPIO.LOW)
