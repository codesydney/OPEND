from flask import render_template, flash, redirect, request, url_for
from app import app, db, models
from .forms import MainForm, ResultForm
from flask_bootstrap import Bootstrap

Bootstrap(app)

#config
import os
app.config.from_object(os.environ['APP_SETTINGS'])
print (os.environ['APP_SETTINGS'])

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
	form = MainForm()
	resultform = ResultForm()
	
	if form.validate_on_submit() and form.Submit1.data:
		InputAddress = form.InputAddress.data
		recs = models.nsw_birth_rates.query.order_by(models.nsw_birth_rates.count.desc()).all()	

		suburb_list = []		
		for rec in recs:
			selected_fields=[rec.year,rec.locality,rec.suburb,rec.state,rec.postcode,rec.count]
			suburb_list.append(selected_fields)		

		return render_template('result.html',
								resultform=resultform,
								InputAddress=InputAddress,
								suburb_list=suburb_list)								
								
	elif resultform.validate_on_submit() and resultform.Submit2.data:	
         return redirect(url_for('index'))
	else:		
	    return render_template('mainform.html',
                                form=form)