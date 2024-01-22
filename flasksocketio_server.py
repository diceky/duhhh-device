from flask import Flask, request, render_template, jsonify
from flask_socketio import SocketIO, join_room
from datetime import datetime
import json
from collections import namedtuple

app = Flask(__name__)
#app.config['SECRET_KEY'] = 'xog046oTS^w0viKAfDzL'
sio = SocketIO(app, cors_allowed_origins='*')   

values = {}

@app.route(f'/api/request-state', methods=['GET'])
def return_state():
    global button1, button2, knob1
    room = request.args.get('room')
    if request.method == 'GET':
        return jsonify({'values': values[room]})

@sio.on('connect', namespace='/duhhh-device')
def handle_connect(auth):
    room = auth['room']
    if not room in values:
        values[room] = {}
    join_room(room)
    print('[{}] connect sid : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), request.sid))
    print('assigning to room: {}'.format(room))

@sio.on('set_state', namespace='/duhhh-device')
def handle_set_state(msg):
    global button1, button2, knob1
    room = msg['room']
    if 'button1' in msg:
        button1 = msg['button1']
        values[room]['button1'] = button1
        response = "button1"
    if 'button2' in msg:
        button2 = msg['button2']
        values[room]['button2'] = button2
        response = "button2"
    if 'knob1' in msg:
        knob1 = msg['knob1']
        values[room]['knob1'] = knob1
        response = "knob1"
    sio.emit('response', f'{response} state updated.', room=request.sid, namespace='/duhhh-device')
    print(f'{response} state updated.')

@sio.on('sid_message', namespace='/duhhh-device')
def handle_sid_message(msg):
    sio.emit('response', msg, room=request.sid, namespace='/duhhh-device')
    print('[{}] emit sid : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , msg))

@sio.on('skip_sid_message', namespace='/duhhh-device')
def handle_skip_sid_message(msg):
    sio.emit('response', msg, skip_sid=request.sid, namespace='/duhhh-device')
    print('[{}] emit skip sid : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , msg))

@sio.on('broadcast_message', namespace='/duhhh-device')
def handle_broadcast_message(msg):
    sio.emit('response', msg, namespace='/duhhh-device')
    print('[{}] emit all : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , msg))

@sio.on('disconnect', namespace='/duhhh-device')
def handle_disconnect():
    print('[{}] disconnect'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

if __name__ == '__main__':
    sio.run(app, host='0.0.0.0', port=3000)