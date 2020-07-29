import socketio
import cv2
import base64
import time


sio = socketio.Client()

connected = False

@sio.event
def connect():
    print('connection established')

@sio.event
def joined(data):
    print('new member joined')
    connected = True
    sio.emit('message', 'Hello from PI')


@sio.event
def disconnect():
    print("Client Disconnected")

@sio.on('message')
def message(data):
    print('{data}, sent message')

sio.connect('http://192.168.0.111:4500')


cap = cv2.VideoCapture(0)

(grabbed, frame) = cap.read()
fshape = frame.shape
fheight = fshape[0]
fwidth = fshape[1]
print(fwidth, fheight)


while True:
    ret, frame = cap.read()
    ret, buffer = cv2.imencode('.jpg', frame)
    jpg_base64 = base64.b64encode(buffer)

    sio.emit('cameraFeed', { 'cameraFeed': jpg_base64.decode('utf-8') })
    
cap.release()
sio.wait()