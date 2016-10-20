#   https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms



#from flask.ext.wtf import Form
from flask_wtf import Form      #   fix. http://stackoverflow.com/questions/20032922/no-module-named-flask-ext-wtf
#from flaskForm import Form
from wtforms import StringField, BooleanField, SelectField
from wtforms.validators import DataRequired

class RelayAddForm(Form):
    #openid = StringField('openid', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    isenable = BooleanField('isenable', default=False)
    # bmcnr = SelectField(label="bmcnr", coerce=int)  #   http://stackoverflow.com/questions/22364551/creating-flask-form-with-selects-from-more-than-one-table
    bmcnr = SelectField(label="bmcnr",  coerce=int)
    #bmcnr = SelectField(label="bmcnr", coerce=int, choices = [('0', 'not')]) 
    #bmcnr = SelectField('bmcnr', choices = [('cpp', 'C++'), ('py', 'Python')])

