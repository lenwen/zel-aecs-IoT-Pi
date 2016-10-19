"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify, redirect, flash
from FlaskWeb import app
from Settings import Settings
import json
from .forms import RelayAddForm


# from FlaskWebProject1 import app

@app.route('/')
#@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )

@app.route('/sensors')
def sensors():
    """Renders the about page."""
    return render_template(
        'sensors.html',
        title='Sensors Title',
        year=datetime.now().year,
        sensdata = Settings.sensors
    )

@app.route('/relays')
def relays():
    """Renders the about page."""
    return render_template(
        'relays.html',
        title='Relay information',
        year=datetime.now().year,
        relaydata = Settings.relays,
        accesskey = Settings.keyAccess
    )

@app.route('/testpage')
def testpage():
    """Renders the home page."""
    return render_template(
        'testpage.html',
        title='Home Page',
        year=datetime.now().year,
        text1=request.args.get('qq')
    )

#sensdata = Settings.sensors
def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/sleoffieh38dewd', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

#   ==============================================================================================
#   Form data requests
#   ----------------------------------------------------------------------------------------------
@app.route('/relays/add', methods=['GET', 'POST'])
def relayadd():
    form = RelayAddForm()
    if form.validate_on_submit():
        flash("hej")
    return render_template('relaysadd.html',
        title='Sign In',
        form=form)

    

#   ==============================================================================================
#   Api requests
#   ----------------------------------------------------------------------------------------------
#   https://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask

@app.route('/api/relay/actions')
def apiRelayActions():
    key = request.args.get('key')
    relayId = request.args.get('relayid')
    options = request.args.get('option')
    pageUrl = request.args.get('page')

    data1 = ""
    data2 = ""
    if key is None:
        data1 = "ingen key"
        return ('', 204)
    else:
        data1 = "key: " + key

    if relayId is not None:
        if int(relayId) not in Settings.relays:
            data2 = "relay dont exist"
        else:
            if options == "on":
                Settings.relays[int(relayId)].TurnOn(False)
                if pageUrl is None:
                    return ('', 204)
                return redirect(pageUrl)
                #Settings.relays[1].TurnOn(False)
            elif options == "off":
                Settings.relays[int(relayId)].TurnOff(False)
                if pageUrl is None:
                    return ('', 204)
                return redirect(pageUrl)
                

         

    """Renders the home page."""
    return render_template(
        'testpage.html',
        title='Home Page',
        year=datetime.now().year,
        text1=data1, text2 = data2
    )

@app.route('/api/relay/v0.1', methods=['GET'])
def apiRelayGet():
    #simplejson.dumps(anyObj, default=lambda obj: obj.__dict__)
    #simplejson.dumps(Settings.relays, default=lambda obj: obj.__dict__)
    #test1 = json.dumps(Settings.relays, default=lambda obj: obj.__dict__)
    #return jsonify({'relays': test1})
    return jsonify({'relays' : json.dumps(Settings.relays, default=lambda obj: obj.__dict__)})

@app.route('/api/sensor/v0.1', methods=['GET'])
def apiSensorGet():
    return jsonify({'sensors' : json.dumps(Settings.sensors, default=lambda obj: obj.__dict__)})
    