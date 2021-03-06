from flask import Flask, render_template, request, redirect, url_for
import socket
import time
import threading


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

HEADER = 64
PORT = 5000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.110"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

DataIn = ''
connected = True
dev_list = []
selDev = ''
speed = 'MED'
step = '75'


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        event = request.form.get('eventSel')
        send(event)
        event = ''
        return redirect(url_for('home'))

    return render_template("index.html")

@app.route('/hook', methods=['GET', 'POST'])
def hook():
    if request.method == 'GET':
        command = request.args.get('comm')
        print(command)
        send(command)
        command = ''
        return redirect(url_for('hook'))

    return render_template("index.html")

@app.route('/remote', methods=['GET', 'POST'])
def remote():
    if request.method == 'POST':
        event = request.form.get('eventSel')
        send(event)
        event = ''
        return redirect(url_for('remote'))

    return render_template("remote.html")

@app.route('/cam', methods=['GET', 'POST'])
def cam():
    global speed
    if request.method == 'POST':
        event = request.form.get('eventSel')
        print(event)
        if (event == 'lvhtpc, low'):
            speed = 'LOW'
        elif (event == 'lvhtpc, med'):
            speed = 'MED'
        elif (event == 'lvhtpc, hi'):
            speed = 'HI'
        send(event)
        event = ''
        return redirect(url_for('cam'))

    return render_template("cam.html", speed=speed)

@app.route('/rview', methods=['GET', 'POST'])
def rview():
    global speed
    if request.method == 'POST':
        event = request.form.get('eventSel')
        print(event)
        if (event == 'rover, cam-clow'):
            speed = 'LOW'
        elif (event == 'rover, cam-cmed'):
            speed = 'MED'
        elif (event == 'rover, cam-chi'):
            speed = 'HI'
        send(event)
        event = ''
        return redirect(url_for('rview'))

    return render_template("roverview.html", speed=speed)

@app.route('/pilot', methods=['GET', 'POST'])
def pilot():
    global speed
    global step
    if request.method == 'POST':
        dir = request.form.get('eventSel')
        step = request.form.get('steps')
        event = dir + step
 
        print(event)
        send(event)
        event = ''
        return redirect(url_for('pilot'))

    return render_template("pilot.html", speed=step)

@app.route('/lvtree', methods=['GET', 'POST'])
def lvtree():
    if request.method == 'POST':
        event = request.form.get('eventSel')
        send(event)
        event = ''
        return redirect(url_for('lvtree'))

    return render_template("lvtree.html")

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global dev_list
    global selDev
    send('site, devices')
    if request.method == 'POST':
        device = request.form.get('sDev')
        event = request.form.get('eventSel')
        send(f"{device}, {event}")
        selDev = device
        device = ''
        event = ''
        return redirect(url_for('admin'))

    return render_template("admin.html", devices=dev_list, selDev=selDev)


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    msg = ''
    
def SocketIn():
    global DataIn
    global connected
    global dev_list
    print('listening...')
    while connected:
        DataIn = client.recv(2048).decode(FORMAT)
        if not DataIn:
            break
        dev_list = DataIn.split(', ')
        DataIn = ''

SockThread = threading.Thread(target=SocketIn, args=())
SockThread.setDaemon(True)
SockThread.start()


send('site')

if __name__ == '__main__':
    app.run(debug=True, port='5055', host='0.0.0.0') 
