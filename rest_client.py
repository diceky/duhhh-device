import json
import RPi.GPIO as GPIO
import requests
from time import sleep

button1Pin = 2
button2Pin = 3
knob1PinA = 17
knob1PinB = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(button1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(knob1PinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(knob1PinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

url = 'http://127.0.0.1:5000/api/set-state'

def button1_pressed(channel):
    if GPIO.input(button1Pin):
        data ={"button1": 0 }
    else:
        data ={"button1": 1 }
    response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
    print(response)

def button2_pressed(channel):
    if GPIO.input(button2Pin):
        data ={"button2": 0 }
    else:
        data ={"button2": 1 }
    response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
    print(response)

GPIO.add_event_detect(button1Pin, GPIO.BOTH, callback=button1_pressed, bouncetime=100)
GPIO.add_event_detect(button2Pin, GPIO.BOTH, callback=button2_pressed, bouncetime=100)

counter = 0
clkLastState = GPIO.input(knob1PinA)

while True:
    clkState = GPIO.input(knob1PinA)
    dtState = GPIO.input(knob1PinB)
    if clkState != clkLastState:
        if dtState != clkState:
            counter += 1
        else:
            counter -= 1
        print(counter)
        data ={"knob1": counter}
        response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
    clkLastState = clkState
    sleep(0.001)
