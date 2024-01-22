import eventlet
import socketio
from datetime import datetime

sio = socketio.Server(cors_allowed_origins='*') # ignore CORS errors

@sio.on('connect', namespace='/device')
def handle_connect(sid, environ):
    print('[{}] connet sid : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , sid))
    print('[{}] connet env : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , environ))

@sio.on('sid_message', namespace='/device')
def handle_sid_message(sid, msg):
    sio.emit('response', msg, room=sid, namespace='/device')
    print('[{}] emit sid : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , msg))

@sio.on('skip_sid_message', namespace='/device')
def handle_skip_sid_message(sid, msg):
    sio.emit('response', msg, skip_sid=sid, namespace='/device')
    print('[{}] emit skip sid : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , msg))

@sio.on('broadcast_message', namespace='/device')
def handle_broadcast_message(sid, msg):
    sio.emit('response', msg, namespace='/device')
    print('[{}] emit all : {}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S') , msg))

@sio.on('disconnect', namespace='/device')
def handle_disconnect(sid):
    print('[{}] disconnect'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))

if __name__ == '__main__':
    app = socketio.WSGIApp(sio) # create wsgi server middleware
    eventlet.wsgi.server(eventlet.listen(('',3000)), app) # start wsgi server
    