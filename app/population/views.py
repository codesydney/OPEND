from flask import Flask, g, request, make_response, redirect, url_for, jsonify, render_template
from . import population
from app.population.database import connect_db_popu
#import json


@population.route('/details', methods=['GET'])
def get_details():
    db = connect_db_popu()
    details_cur = db.execute('select YEAR, CODE, SUBURB, STATE, POSTCODE, POPULATION from NSW_POPULATION')
    details = details_cur.fetchall()

    return_values = []

    for detail in details:
        detail_dict = {}
        detail_dict['YEAR']      = detail['YEAR']
        detail_dict['CODE']  = detail['CODE']
        detail_dict['SUBURB']    = detail['SUBURB']
        detail_dict['STATE']     = detail['STATE']
        detail_dict['POSTCODE']  = detail['POSTCODE']
        detail_dict['POPULATION']     = detail['POPULATION']

        return_values.append(detail_dict)

    return jsonify({'details' : return_values})

@population.route('/details/<string:SUBURB>', methods=['GET'])
def get_detail(SUBURB):
    print("==>app/population/views.py: enter")
    db = connect_db_popu()

    # db_path = "C:\\D\\LB_2017\\Computer\\GitHub\\OPEND\\app\\population\\NSW_POPULATION.sqlite"
    # sql = sqlite3.connect(db_path)
    # sql.row_factory = sqlite3.Row
    # db = sql

    print("===>population/views.py:: suburb = "+SUBURB)
    lowsubburb = SUBURB.lower()
    details_cur = db.execute('select YEAR, CODE, SUBURB, STATE, POSTCODE, POPULATION from NSW_POPULATION where SUBURB = ?', [lowsubburb])
    details = details_cur.fetchall()

    return_values = []

    for detail in details:
        detail_dict = {}
        detail_dict['YEAR']      = detail['YEAR']
        detail_dict['CODE']  = detail['CODE']
        detail_dict['SUBURB']    = detail['SUBURB']
        detail_dict['STATE']     = detail['STATE']
        detail_dict['POSTCODE']  = detail['POSTCODE']
        detail_dict['POPULATION']     = detail['POPULATION']
        #print("===>population/views.py:: POPULATION = "+detail_dict['POPULATION'])
        return_values.append(detail_dict)

    return jsonify({'details' : return_values})
