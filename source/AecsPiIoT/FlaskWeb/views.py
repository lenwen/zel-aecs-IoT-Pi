"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, jsonify, redirect, flash
from FlaskWeb import app
from .forms import RelayAddForm

import sqlite3
from Settings import Settings
from DatabaseHandling import dbTblGpioLayout, dbTblRelays
import json

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
        nodename=Settings.nodeName,
        relaydata = Settings.relays,
        accesskey = Settings.keyAccess
    )

@app.route('/relays/nofreegpios')
def relaysnofreegrio():
    """Renders the about page."""
    return render_template(
        'relaysnofreegpios.html',
        title='Relay information - No Free Gpio Exist',
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

    errorInForm = False

    bmcnrValues = dbTblGpioLayout.dbTblGpioLayout.GetFreeGpioPortAsSelectedList()
        
    if bmcnrValues is None:
        return redirect("/relays/nofreegpios")

    form.relbmcnr.choices = bmcnrValues

    

    
    while form.validate_on_submit():
        if form.relstartason.data is True:
            if form.relstartaslastvalue.data is True:
                #   Error. relay canot be true in this 2 options
                errorInForm = True
                form.relstartason.errors.append("This cannot be selected when (start whit last value is selected)!!!")
                form.relstartaslastvalue.errors.append("This cannot be selected when (start as on is selected)!!!")
                break
        print("port: " + str(form.relbmcnr.data))
        print("type: " + str(form.reltype.data))
        #   Check if Pi physical port is stile free.
        if dbTblGpioLayout.dbTblGpioLayout.IsPhysicalPortFree(str(form.relbmcnr.data)) is False:
            #   Port is not free. show error
            form.relbmcnr.errors.append("There is an error whit selected port. Select another port!")
            break
        
        #   Set Physical port in use
        dbTblGpioLayout.dbTblGpioLayout.SetPhysicalPortInUseStatus(str(form.relbmcnr.data), True)

        print("hej")

        #   Add relay information to database.
        relayId = dbTblRelays.dbTblRelays.AddRelay(str(form.relbmcnr.data),str(form.reltype.data),"1",form.relenable.data,form.relstartason.data, form.relstartaslastvalue.data, False, form.relname.data, form.relnameinfo.data)
        break

        #flash("hej")

        #   select * from tblgpiolayout where inuse = 0 and name like "GPIO%" order by bcm
         
    return render_template('relaysadd.html',
        title='Register new relay',
        nodename=Settings.nodeName,
        form=form)


    #state_names = []

    

    #for row in rows::
    #    state_names.append(row[0])
        

#    >>> combs = []
#>>> for x in [1,2,3]:
#...     for y in [3,1,4]:
#...         if x != y:
#...             combs.append((x, y))
#...
#>>> combs
#[(1, 3), (1, 4), (2, 3), (2, 1), (2, 4), (3, 1), (3, 4)]
    
    #state_choices = list(enumerate(state_names))    
    
    #form.bmcnr.choices = state_choices
    
    


    

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
    