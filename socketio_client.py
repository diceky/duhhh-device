import socketio
import time
from datetime import datetime
import RPi.GPIO as GPIO

deviceID = "000001"

button1Pin = 2
button2Pin = 3
knob1PinA = 17
knob1PinB = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(button1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(knob1PinA, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(knob1PinB, GPIO.IN, pull_up_down=GPIO.PUD_UP)

counter = 0
clkLastState = GPIO.input(knob1PinA)

sio = socketio.Client()

def button1_pressed(channel):
    if GPIO.input(button1Pin):
        data = {
            "button1": 0,
            "room": deviceID
        }
    else:
        data = {
            "button1": 1,
            "room": deviceID
        }
    sio.emit('set_state', data, namespace='/duhhh-device')

def button2_pressed(channel):
    if GPIO.input(button2Pin):
        data = {
            "button2": 0,
            "room": deviceID
        }
    else:
        data = {
            "button2": 1,
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

def background_task():
    global counter, clkLastState
    while True:
        clkState = GPIO.input(knob1PinA)
        dtState = GPIO.input(knob1PinB)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
            else:
                counter -= 1
            data = {
                "knob1": counter,
                "room": deviceID
            }
            sio.emit('set_state', data, namespace='/duhhh-device')
        clkLastState = clkState
        sio.sleep(0.001)

task = sio.start_background_task(background_task)

auth = {
    "room": deviceID
}
sio.connect('http://192.168.11.11:3000', namespaces=['/duhhh-device'], auth=auth)
sio.wait()
        
