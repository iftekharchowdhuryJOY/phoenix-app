import socket
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    hostname = socket.gethostname()
    return f"""
    <div style="text-align: center; margin-top: 50px; font-family: sans-serif;">
        <h1 style="color:green;">🦅 The Phoenix is RISING! 🦅</h1>
        <h2>Running on Server: <span style="color:blue;">{hostname}</span></h2>
        <p>Version: 1.0</p>
    </div>
    """

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)