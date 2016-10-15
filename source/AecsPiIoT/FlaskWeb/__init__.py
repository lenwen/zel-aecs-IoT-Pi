"""
The flask application package.
"""
import requests
import urllib.parse
from os import environ
import threading
from flask import Flask
app = Flask(__name__)
import FlaskWeb.views
from flask import request
from Settings import Settings

class WebSite (threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self)
        self.name = name

    def run(self):
        #HOST = environ.get('SERVER_HOST', 'localhost')
        try:
            #PORT = int(environ.get('SERVER_PORT', '5555'))
            PORT = int(environ.get('SERVER_PORT', Settings.webSitePort ))
        except ValueError:
            PORT = 5555
        #app.run(HOST, PORT)
        app.run('0.0.0.0', PORT, None )


    
    #def shutdown_server(self):
    #    func = request.environ.get('werkzeug.server.shutdown')
    #    if func is None:
    #        raise RuntimeError('Not running with the Werkzeug Server')
    #    func()

    def stop(self):
        urltostop = "http://localhost:" + str(Settings.webSitePort) + "/sleoffieh38dewd" 
        requests.post(urltostop)
        #self.shutdown_server()
        print("sdfdsf")