from flask import Flask, render_template
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)


@app.route('/')
def home():
    return render_template("index.html")


if __name__ == '__main__':
    socketio.run(app, debug=True, port='5055', host='0.0.0.0')
