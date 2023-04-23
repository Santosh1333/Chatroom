from flask import Flask, render_template, request
import socket

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('App.html')

@app.route('/chat', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        message = request.form['message']
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('127.0.0.1', 5000))
            s.sendall(message.encode())
    return render_template('chat.html')
