#   https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms



#from flask.ext.wtf import Form
from flask_wtf import Form      #   fix. http://stackoverflow.com/questions/20032922/no-module-named-flask-ext-wtf
#from flaskForm import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired

class RelayAddForm(Form):
    #openid = StringField('openid', validators=[DataRequired()])
    relname = StringField('relname', validators=[DataRequired()])
    relnameinfo = StringField('relnameinfo')
    relenable = BooleanField('relenable', default=False)
    relstartason = BooleanField('relstartason', default=False)
    relstartaslastvalue = BooleanField('relstartaslastvalue', default=False)
    # bmcnr = SelectField(label="bmcnr", coerce=int)  #   http://stackoverflow.com/questions/22364551/creating-flask-form-with-selects-from-more-than-one-table
    relbmcnr = SelectField(label="relbmcnr",  coerce=int)
    reltype = SelectField(label="reltype", choices = [('1', 'Off = High signal (1) | On = low signal(0)'), ('2', 'Off = Low signal (0) | On = High signal(0)')])
    #bmcnr = SelectField(label="bmcnr", coerce=int, choices = [('0', 'not')]) 
    #bmcnr = SelectField('bmcnr', choices = [('cpp', 'C++'), ('py', 'Python')])

class SensorEditForm(Form):
    #sensorformispostback = None
    sensortype = SelectField(label="sensortype",  coerce=int)
    sensortypedata = None
    sensorenable = BooleanField('sensorenable', default=True)
    sensorname =  StringField('sensorname', validators=[DataRequired()])
    sensorinfo = StringField('sensorinfo')
    sensorcollecttime = StringField('sensorcollecttime', validators=[DataRequired()])
    sensorsaverealtimetodatabase = BooleanField('sensorsaverealtimetodatabase', default=False)
    sensorsavehistorytodatabase = BooleanField('sensorsavehistorytodatabase', default=False)


