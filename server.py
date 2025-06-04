# server.py
# Socket.IO backend server for Secure AES Chat Box

import socketio
import eventlet
from eventlet import wsgi
from flask import Flask

# Create Socket.IO server with CORS allowed for all origins
sio = socketio.Server(cors_allowed_origins='*')
app = Flask(__name__)
app = socketio.WSGIApp(sio, app)

@sio.event
def connect(sid, environ):
    print('User connected:', sid)

@sio.event
def chat_message(sid, data):
    # Data format: { sender: str, encryptedMessage: str }
    # Broadcast message to all except sender
    sio.emit('chat_message', data, skip_sid=sid)

@sio.event
def disconnect(sid):
    print('User disconnected:', sid)

if __name__ == '__main__':
    port = 3000
    print(f'Starting Secure AES Chat backend server on http://localhost:{port}')
    eventlet.wsgi.server(eventlet.listen(('', port)), app)

