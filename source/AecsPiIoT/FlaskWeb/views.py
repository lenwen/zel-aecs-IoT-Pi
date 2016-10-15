"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request
from FlaskWeb import app
from Settings import Settings

# from FlaskWebProject1 import app

@app.route('/')
@app.route('/home')
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
