from flask import render_template, flash, redirect, request, url_for, jsonify, Response
from app import db, bootstrap
from . import main 
from .models import nsw_birth_rates
from .forms import MainForm, ResultForm
#from flask_bootstrap import Bootstrap
import json
import urllib.request

#Bootstrap(main)

#config
#import os
#main.config.from_object(os.environ['APP_SETTINGS'])
#print (os.environ['APP_SETTINGS'])

@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
	form = MainForm()
	resultform = ResultForm()
	
	if form.validate_on_submit() and form.Submit1.data:
		InputSuburb = form.InputSuburb.data

		#************* BEGIN - NSW Birth Rate Information API Call ****************** 
		birth_rate_url = "http://codesydneyopend.herokuapp.com/details/"+InputSuburb
		print (birth_rate_url)
		request = urllib.request.Request(birth_rate_url)
		my_response = urllib.request.urlopen(request)
		json_response = json.load(my_response)

		value_details = []
		value_details = json_response.get('details')

		birth_rate_list = []
		for d in value_details:
			selected_fields=[d['YEAR'],d['LOCALITY'],d['SUBURB'],d['STATE'],d['POSTCODE'],d['COUNT']]
			birth_rate_list.append(selected_fields)		
		#************ END- NSW Birth Rate Information API Call **********************

		#************* BEGIN - NSW Population Information API Call ****************** 
		population_url = "https://nswpopulation20171121.herokuapp.com/details/"+InputSuburb
		request = urllib.request.Request(population_url)
		my_response_popu = urllib.request.urlopen(request)
		json_response_popu = json.load(my_response_popu)
		print(json_response_popu)

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
         return redirect(url_for('index'))
	else:		
	    return render_template('mainform.html',
                                form=form)

@main.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    query = db.session.query(nsw_birth_rates.suburb).filter(nsw_birth_rates.suburb.ilike("%"+str(search)+"%"))	
    #query = db.session.query(models.nsw_birth_rates.suburb).filter(models.nsw_birth_rates.suburb.ilike("%"+str(search)+"%"))	
    #query = db.session.query(nsw_birth_rates.suburb).filter(nsw_birth_rates.suburb.ilike("%"+"a"+"%"))	
    results = [mv[0] for mv in query.all()]
    return jsonify(matching_results=results)
    