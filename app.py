import subprocess

from flask import Flask
app = Flask(__name__)

def run_command(command):
    return subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()

@app.route('/<command>')
def command_server(command):
    return run_command(command)
