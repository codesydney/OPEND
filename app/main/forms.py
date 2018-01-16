from flask_wtf import FlaskForm
#from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SubmitField, HiddenField
from wtforms import validators
from wtforms.validators import DataRequired
from werkzeug.datastructures import MultiDict

class MainForm(FlaskForm):
	OpendTitle = StringField("OPEND")
	InputAddress = StringField('Input your address',[validators.Required("Enter your address")])	
	Submit1 = SubmitField('Get Report',render_kw={"size":"90"})	    

class ResultForm(FlaskForm):
    Submit2 = SubmitField('Try again',render_kw={"size":"90"})