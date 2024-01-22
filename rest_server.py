from flask import Flask, request, jsonify
import json
import requests
from time import sleep

app = Flask(__name__)

button1 = 0
button2 = 0
knob1 = 0

button1Pin = 2
button2Pin = 3
knob1PinA = 17
knob1PinB = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(button1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(knob1PinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(knob1PinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def button1_pressed(channel):
    if GPIO.input(button1Pin):
        button1 = 0
    else:
        button1 = 1

def button2_pressed(channel):
    if GPIO.input(button2Pin):
        button2 = 0
    else:
        button2 = 1

GPIO.add_event_detect(button1Pin, GPIO.BOTH, callback=button1_pressed, bouncetime=100)
GPIO.add_event_detect(button2Pin, GPIO.BOTH, callback=button2_pressed, bouncetime=100)

counter = 0
clkLastState = GPIO.input(knob1PinA)

def background_loop():
    global counter, clkLastState
    while True:
        clkState = GPIO.input(knob1PinA)
        dtState = GPIO.input(knob1PinB)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
            else:
                counter -= 1
            knob1 = counter
        clkLastState = clkState
        sleep(0.001)

@app.route('/api/request-state', methods=['GET'])
def return_state():
    global button1, button2, knob1
    if request.method == 'GET':
        values = {
            'button1': button1,
            'button2': button2,
            'knob1': knob1,
        }
        return jsonify({'values': values})

# @app.route('/api/set-state', methods=['POST'])
# def set_state():
#     global button1, button2, knob1
#     if request.method == 'POST':
#         content = request.json
#         if 'button1' in content:
#             button1 = content['button1']
#         if 'button2' in content:
#             button2 = content['button2']
#         if 'knob1' in content:
#             knob1 = content['knob1']
#         print(button1, button2, knob1)
#         return 'OK'

if __name__ == "__main__":
    app.run(host='0.0.0.0') #make server publicly available on same network    
