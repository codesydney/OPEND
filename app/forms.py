from flask_wtf import Form
from flask.ext.wtf import Form
from wtforms import StringField, IntegerField, SubmitField, HiddenField
from wtforms import validators
from wtforms.validators import DataRequired
from werkzeug.datastructures import MultiDict

class MainForm(Form):
	OpendTitle = StringField("OPEND")
	InputAddress = StringField('Address', [validators.Required("Please enter your address.")],render_kw={"placeholder": "","size":"10"})	
	Submit1 = SubmitField('Submit',render_kw={"size":"90"})	    

class ResultForm(Form):
    Submit2 = SubmitField('Try again',render_kw={"size":"90"})	 