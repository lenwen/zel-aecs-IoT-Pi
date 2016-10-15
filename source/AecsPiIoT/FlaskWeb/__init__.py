"""
The flask application package.
"""
from os import environ
import threading
from flask import Flask
app = Flask(__name__)
import FlaskWeb.views

class WebSite (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        HOST = environ.get('SERVER_HOST', 'localhost')
        try:
            PORT = int(environ.get('SERVER_PORT', '5555'))
        except ValueError:
            PORT = 5555
        app.run(HOST, PORT)

    def stop(self):
        print("sdfdsf")
    