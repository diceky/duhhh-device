from flask import Flask, request, jsonify
import json
from time import sleep

app = Flask(__name__)

button1 = 0
button2 = 0
knob1 = 0


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
