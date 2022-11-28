from flask import Flask
app = Flask(__name__)

@app.route("/index")
def hello():
    return "Hello, World!"
