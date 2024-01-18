from flask import Flask, request, jsonify
import json
import RPi.GPIO as GPIO
import requests

app = Flask(__name__)

button1 = 0
button2 = 0
knob1 = 0

button1Pin = 2
button2Pin = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(button1Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(button2Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

url = 'http://127.0.0.1:5000/api/set-state'

def button1Pressed(channel):
    if GPIO.input(button1Pin):
        data ='{"button1": 0 }'
    else:
        data ='{"button1": 1 }'
    response = requests.post(url, data=data,headers={"Content-Type": "application/json"})
    print(response)

def button2Pressed(channel):
    if GPIO.input(button2Pin):
        data ='{"button2": 0 }'
    else:
        data ='{"button2": 1 }'
    response = requests.post(url, data=data,headers={"Content-Type": "application/json"})
    print(response)

GPIO.add_event_detect(button1Pin, GPIO.BOTH, callback=button1Pressed, bouncetime=100)
GPIO.add_event_detect(button2Pin, GPIO.BOTH, callback=button2Pressed, bouncetime=100)

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
    app.run(host='0.0.0.0') #make server publicly available on same network
