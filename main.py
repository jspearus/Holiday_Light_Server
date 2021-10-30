from flask import Flask, render_template, request, redirect, url_for
import socket
import time


app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'

HEADER = 64
PORT = 5000
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "dgscore.ddns.net"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        event = request.form.get('eventSel')
        send(event)
        event = ''
        return redirect(url_for('home'))

    return render_template("index.html")


def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    msg = ''


send('site')

if __name__ == '__main__':
    app.run(debug=True, port='5055', host='0.0.0.0')
