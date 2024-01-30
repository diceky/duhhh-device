from flask import Flask, request, jsonify
import json
import requests
from time import sleep
import RPi.GPIO as GPIO
import threading
import socketio
from datetime import datetime

app = Flask(__name__)

deviceID = "000001"

button1 = 0
button2 = 0
knob1 = 0

button1Pin = 2
button2Pin = 3
knob1PinA = 17
knob1PinB = 18

sio = socketio.Client()

GPIO.setmode(GPIO.BCM)
GPIO.setup(button1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(knob1PinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(knob1PinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
clkLastState = GPIO.input(knob1PinA)

def button1_pressed(channel):
    global button1
    if GPIO.input(button1Pin):
        button1 = 0
    else:
        button1 = 1
    data = {
            "button1": button1,
            "room": deviceID
        }
    sio.emit('set_state', data, namespace='/duhhh-device')

def button2_pressed(channel):
    global button2
    if GPIO.input(button2Pin):
        button2 = 0
    else:
        button2 = 1
    data = {
            "button2": button2,
            "room": deviceID
        }
    sio.emit('set_state', data, namespace='/duhhh-device')

GPIO.add_event_detect(button1Pin, GPIO.BOTH, callback=button1_pressed, bouncetime=100)
GPIO.add_event_detect(button2Pin, GPIO.BOTH, callback=button2_pressed, bouncetime=100)

@sio.on('connect', namespace='/duhhh-device')
def handle_connect():
    print('[{}] connect'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

@sio.on('disconnect', namespace='/duhhh-device')
def handle_disconnect():
    print('[{}] disconnect'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

@sio.on('response', namespace='/duhhh-device')
def handle_response(msg):
    print('[{}] response : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , msg))

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

def server():
    app.run(host='0.0.0.0', use_reloader=False, port=5000)

if __name__ == "__main__":
    
    threading.Thread(target=server, daemon=True).start()

    auth = {
        "room": deviceID
    }
    sio.connect('https://mood-checker-server.herokuapp.com', namespaces=['/duhhh-device'], auth=auth)

    while True:
        clkState = GPIO.input(knob1PinA)
        dtState = GPIO.input(knob1PinB)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
            else:
                counter -= 1
            knob1 = counter
            data = {
                "knob1": counter,
                "room": deviceID
            }
            sio.emit('set_state', data, namespace='/duhhh-device')
        clkLastState = clkState
        sleep(0.001)

