from flask import Flask, request, jsonify
import json
import RPi.GPIO as GPIO
import requests
from multiprocessing import Process, Value
from time import sleep
import aiohttp
import asyncio

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

url = 'http://127.0.0.1:5000/api/set-state'

def button1_pressed(channel):
    if GPIO.input(button1Pin):
        data ='{"button1": 0 }'
    else:
        data ='{"button1": 1 }'
    response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
    #print(response)

def button2_pressed(channel):
    if GPIO.input(button2Pin):
        data ='{"button2": 0 }'
    else:
        data ='{"button2": 1 }'
    response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
    #print(response)

GPIO.add_event_detect(button1Pin, GPIO.BOTH, callback=button1_pressed, bouncetime=100)
GPIO.add_event_detect(button2Pin, GPIO.BOTH, callback=button2_pressed, bouncetime=100)

counter = 0
clkLastState = GPIO.input(knob1PinA)

async def async_post(data):
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=url,
                                      data=data,
                                      headers={"Content-Type": "application/json"})
        #await print(response)

def background_loop():
    global url, counter, clkLastState
    while True:
        clkState = GPIO.input(knob1PinA)
        dtState = GPIO.input(knob1PinB)
        if clkState != clkLastState:
            if dtState != clkState:
                counter += 1
            else:
                counter -= 1
            print(counter)
            data ='{"knob1": ' + str(counter) + '}'
            #response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
            asyncio.run(async_post(data))
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

@app.route('/api/set-state', methods=['POST'])
def set_state():
    global button1, button2, knob1
    if request.method == 'POST':
        content = request.json
        if 'button1' in content:
            button1 = content['button1']
        if 'button2' in content:
            button2 = content['button2']
        if 'knob1' in content:
            knob1 = content['knob1']
        print(button1, button2, knob1)
        return 'OK'

if __name__ == "__main__":
    #app.run(host='0.0.0.0') #make server publicly available on same network    
    p = Process(target=background_loop)
    p.start()  
    app.run(host='0.0.0.0', use_reloader=False)
    p.join()
