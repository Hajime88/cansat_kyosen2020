import RPi.GPIO as GPIO
import time

red_pin = 26
green_pin = 6
blue_pin = 13

GPIO.setmode(GPIO.BCM)
GPIO.setup(red_pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(green_pin, GPIO.OUT, initial = GPIO.LOW)
GPIO.setup(blue_pin, GPIO.OUT, initial = GPIO.LOW)

def red_light():
    GPIO.output(red_pin, GPIO.HIGH)
    time.sleep(2.0)
    GPIO.output(red_pin, GPIO.LOW)
    time.sleep(2.0)   

def green_light():
    GPIO.output(green_pin, GPIO.HIGH)
    time.sleep(2.0)
    GPIO.output(green_pin, GPIO.LOW)
    time.sleep(2.0)

def blue_light():
    GPIO.output(blue_pin, GPIO.HIGH)
    time.sleep(2.0)
    GPIO.output(blue_pin, GPIO.HIGH)
    time.sleep(2.0)