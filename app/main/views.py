from flask import render_template, flash, redirect, request, url_for, jsonify, Response, current_app 
from app import db, bootstrap
from . import main 
from .models import nsw_addresses
from .forms import MainForm, ResultForm
import json
import urllib.request
from app.population import views as population_views
from app.birthrate import views as birthrate_views

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
	print("==>main/views.py::index: enter")
	form = MainForm()
	resultform = ResultForm()
	
	if form.validate_on_submit() and form.Submit1.data:
		InputAddress = form.InputAddress.data

		#************* Get the suburb name of the chosen address ****************** 
		query= db.session.query(nsw_addresses.locality_name).filter(nsw_addresses.address.ilike(InputAddress))
		suburblist = []
		for mv in query.all():
			suburblist.append(mv[0])		
		InputSuburb = suburblist[0]	

		#************* BEGIN - NSW Birth Rate Information API Call ****************** 
		my_response_birth = birthrate_views.get_detail(InputSuburb)
		json_response_birth = json.loads(my_response_birth.get_data())
		value_details = []
		value_details = json_response_birth.get('details')

		birth_rate_list = []
		for d in value_details:
			selected_fields=[d['YEAR'],d['LOCALITY'],d['SUBURB'],d['STATE'],d['POSTCODE'],d['COUNT']]
			birth_rate_list.append(selected_fields)		
		#************ END- NSW Birth Rate Information API Call **********************

		#************* BEGIN - NSW Population Information API Call ****************** 
		my_response_popu = population_views.get_detail(InputSuburb)
		json_response_popu = json.loads(my_response_popu.get_data())
		value_details = []
		value_details = json_response_popu.get('details')

		population_list = []
		for d in value_details:
			print("line 51",d)
			selected_fields=[d['YEAR'],d['CODE'],d['SUBURB'],d['STATE'],d['POSTCODE'],d['POPULATION']]
			population_list.append(selected_fields)
		#************ END- NSW Population Information API Call **********************
		print("line 54",population_list)

		return render_template('result.html',
								resultform=resultform,
								InputSuburb=InputSuburb,
								birth_rate_list=birth_rate_list,
                                population_list=population_list)								
								
	elif resultform.validate_on_submit() and resultform.Submit2.data:	
         return redirect(url_for('main.index'))
	else:		
	    return render_template('mainform.html',
                                form=form)

@main.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = db.session.query(nsw_addresses.address).filter(nsw_addresses.address.ilike("%"+str(search)+"%")).limit(10)	
    addresslist = []
    for mv in query.all():
    	addresslist.append(mv[0])
    return jsonify(matching_results=addresslist)