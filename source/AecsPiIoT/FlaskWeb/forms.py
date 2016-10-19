#   https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iii-web-forms



#from flask.ext.wtf import Form
from flask_wtf import Form      #   fix. http://stackoverflow.com/questions/20032922/no-module-named-flask-ext-wtf
#from flaskForm import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class RelayAddForm(Form):
    #openid = StringField('openid', validators=[DataRequired()])
    name = StringField('name', validators=[DataRequired()])
    isenable = BooleanField('isenable', default=False)

