from flask import render_template, flash, redirect, request, url_for, jsonify, Response, current_app 
from app import bootstrap, arguments #,db
from . import main 
#from .models import nsw_addresses
from .forms import MainForm, TryAgainForm
#from .mapfuncs import get_boundary
import json
import urllib.request
from app.population import views as population_views
from app.birthrate import views as birthrate_views
#from sqlalchemy import text


from datetime import datetime
import ast
import psycopg2
import psycopg2.extras
from psycopg2.pool import ThreadedConnectionPool
from psycopg2.extensions import AsIs
from contextlib import contextmanager

'''
#########################################
# The following codes are for maps
#########################################
# set command line arguments
args = arguments.set_arguments()

# get settings from arguments
settings = arguments.get_settings(args)

# create database connection pool
pool = ThreadedConnectionPool(
    10, 30,
    database=settings["pg_db"],
    user=settings["pg_user"],
    password=settings["pg_password"],
    host=settings["pg_host"],
    port=settings["pg_port"])

# get the boundary name that suits each (tiled map) zoom level and its minimum value to colour in
def get_boundary(zoom_level):
'''
    '''
    if zoom_level < 7:
        boundary_name = "ste"
        min_display_value = 2025
    elif zoom_level < 9:
        boundary_name = "sa4"
        min_display_value = 675
    elif zoom_level < 11:
        boundary_name = "sa3"
        min_display_value = 225
    elif zoom_level < 14:
        boundary_name = "sa2"
        min_display_value = 75
    elif zoom_level < 17:
        boundary_name = "sa1"
        min_display_value = 25
    else:
        boundary_name = "mb"
        min_display_value = 5

    return boundary_name, min_display_value


    #BinLiu: alway show suburb boundary.
    return "ssc",5

@contextmanager
def get_db_connection():
    """
    psycopg2 connection context manager.
    Fetch a connection from the connection pool and release it.
    """
    try:
        connection = pool.getconn()
        yield connection
    finally:
        pool.putconn(connection)


@contextmanager
def get_db_cursor(commit=False):
    """
    psycopg2 connection.cursor context manager.
    Creates a new cursor and closes it, committing changes if specified.
    """
    with get_db_connection() as connection:
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        try:
            yield cursor
            if commit:
                connection.commit()
        finally:
            cursor.close()

#########################################
## The above codes are for maps
#########################################
'''
@main.route('/', methods=['GET', 'POST'])
@main.route('/index', methods=['GET', 'POST'])
def index():
    print("==>main/views.py::index: enter")
    form = MainForm()
    tryagainform = TryAgainForm()
    
    if form.validate_on_submit() and form.Submit1.data:
        InputAddress = form.InputAddress.data

        #************* Get the suburb name and mb code of the chosen address ****************** 
        with get_db_cursor() as pg_cur:

            sql_template = "SELECT add.locality_name, add.mb_2016_code " \
                "from {0}.nsw_addresses as add " \
                "where add.address ilike '%s' " \
                .format(settings['default_schema'])
            sql = pg_cur.mogrify(sql_template, (AsIs(InputAddress),))            

            print("views.py::index line 120: ",end=' ')
            print(sql)

            try:
                pg_cur.execute(sql)
            except psycopg2.Error:
                return "I can't SELECT:<br/><br/>" + sql

            rows = pg_cur.fetchall()

            #if there is no address in table matched this input value.
            if not rows:
                print("views.py::index: The result of address is empty")
                return render_template('mainform.html', form=tryagainform)

            for row in rows:
                InputSuburb = row['locality_name']
                mb_2016_code = row['mb_2016_code']

            #get ssc code from mb code
            #I seperate this query from the above one 
            #because different year may have different correspondence between suburb and other area.
            sql_template = "SELECT ms.ssc_code " \
                "from {0}.mb_ssc_2016 as ms " \
                "where mb_code_2016 = ( '%s') " \
                .format(settings['default_schema'])
            sql = pg_cur.mogrify(sql_template, (AsIs(mb_2016_code),))            

            print("views.py::index line 154: ",end=' ')
            print(sql)

            try:
                pg_cur.execute(sql)
            except psycopg2.Error:
                return "I can't SELECT:<br/><br/>" + sql

            rows = pg_cur.fetchall()

            #if there is no address in table matched this input value.
            if not rows:
                print("views.py::index: The result of address is empty")
                return render_template('mainform.html', form=tryagainform)

            for row in rows:
                InputSSC = row['ssc_code']

        print("view.py::index: InputSSC = "+InputSSC)


        #************* BEGIN - NSW Birth Rate Information API Call ****************** 
        my_response_birth = birthrate_views.get_detail(InputSuburb)
        #print(my_response_birth.get_data().decode("utf-8"))
        json_response_birth = json.loads(my_response_birth.get_data().decode("utf-8"))
        value_details = []
        value_details = json_response_birth.get('details')

        birth_rate_list = []
        for d in value_details:
            selected_fields=[d['YEAR'],d['LOCALITY'],d['SUBURB'],d['STATE'],d['POSTCODE'],d['COUNT']]
            birth_rate_list.append(selected_fields)     
        #************ END- NSW Birth Rate Information API Call **********************

        #************* BEGIN - NSW Population Information API Call ****************** 
        my_response_popu = population_views.get_detail(InputSuburb)
        json_response_popu = json.loads(my_response_popu.get_data().decode("utf-8"))
        value_details = []
        value_details = json_response_popu.get('details')

        population_list = []
        for d in value_details:
            selected_fields=[d['YEAR'],d['CODE'],d['SUBURB'],d['STATE'],d['POSTCODE'],d['POPULATION']]
            population_list.append(selected_fields)
        #************ END- NSW Population Information API Call **********************

        return render_template('result.html',
                                #resultform=resultform,
                                InputSuburb=InputSuburb,
                                birth_rate_list=birth_rate_list,
                                population_list=population_list,
                                mb_2016_code=mb_2016_code,
                                InputSSC=InputSSC,
                                stats="g1")                             
                                
    #elif resultform.validate_on_submit() and resultform.Submit2.data:   
         #return redirect(url_for('main.index'))
    else:       
        return render_template('mainform.html',
                                form=form)

@main.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    with get_db_cursor() as pg_cur:

        sql_template = "SELECT nsw_addresses.address " \
            "from {0}.nsw_addresses " \
            "where tsv_address @@ plainto_tsquery('%s') " \
            "limit 5 ".format(settings['default_schema'])
        sql = pg_cur.mogrify(sql_template, (AsIs(search),))            

        print("views.py::autocomplete: ",end=' ')
        print(sql)

        try:
            pg_cur.execute(sql)
        except psycopg2.Error:
            return "I can't SELECT:<br/><br/>" + sql

        # Retrieve the results of the query
        rows = pg_cur.fetchall()

    addresslist = []
    for row in rows:
        addresslist.append(row['address'])
    return jsonify(matching_results=addresslist)

#######################################
# the following is for showing the map
#######################################
@main.route("/get-bdy-names")
def get_boundary_name():
    # Get parameters from querystring
    min_val = int(request.args.get('min'))
    max_val = int(request.args.get('max'))

    boundary_zoom_dict = dict()

    for zoom_level in range(min_val, max_val + 1):
        boundary_dict = dict()
        boundary_dict["name"], boundary_dict["min"] = get_boundary(zoom_level)
        boundary_zoom_dict["{0}".format(zoom_level)] = boundary_dict

    return Response(json.dumps(boundary_zoom_dict), mimetype='application/json')


@main.route("/get-metadata")
def get_metadata():
    full_start_time = datetime.now()
    # start_time = datetime.now()

    # Get parameters from querystring

    # # census year
    # census_year = request.args.get('c')

    # comma separated list of stat ids (i.e. sequential_ids) AND/OR equations contains stat ids
    raw_stats = request.args.get('stats')

    # get number of map classes
    try:
        num_classes = int(request.args.get('n'))
    except TypeError:
        num_classes = 7

    # replace all maths operators to get list of all the stats we need to query for
    search_stats = raw_stats.upper().replace(" ", "").replace("(", "").replace(")", "") \
        .replace("+", ",").replace("-", ",").replace("/", ",").replace("*", ",").split(",")

    # TODO: add support for numbers in equations - need to strip them from search_stats list

    # equation_stats = raw_stats.lower().split(",")

    # print(equation_stats)
    # print(search_stats)

    # get stats tuple for query input (convert to lower case)
    search_stats_tuple = tuple([stat.lower() for stat in search_stats])

    # get all boundary names in all zoom levels
    boundary_names = list()
    test_names = list()

    for zoom_level in range(0, 16):
        bdy_name, min_val = get_boundary(zoom_level)

        # only add if bdy not in list
        if bdy_name not in test_names:
            bdy_dict = dict()
            bdy_dict["name"] = bdy_name
            bdy_dict["min"] = min_val
            boundary_names.append(bdy_dict)

            test_names.append(bdy_name)

    # get stats metadata, including the all important table number and map type (raw values based or normalised by pop)
    sql = "SELECT lower(sequential_id) AS id, " \
          "lower(table_number) AS \"table\", " \
          "replace(long_id, '_', ' ') AS description, " \
          "column_heading_description AS type, " \
          "CASE WHEN lower(sequential_id) = '{0}' " \
          "OR lower(long_id) LIKE '%%median%%' " \
          "OR lower(long_id) LIKE '%%average%%' " \
          "THEN 'values' " \
          "ELSE 'percent' END AS maptype " \
          "FROM {1}.metadata_stats " \
          "WHERE lower(sequential_id) IN %s " \
          "ORDER BY sequential_id".format(settings['population_stat'], settings["data_schema"])

    print("views.py::get_metadata: ",end=' ')
    print(sql)
    
    #with db.engine as pg_cur:
    with get_db_cursor() as pg_cur:
        try:
            pg_cur.execute(sql, (search_stats_tuple,))
        except psycopg2.Error:
            return "I can't SELECT:<br/><br/>" + sql

        # Retrieve the results of the query
        rows = pg_cur.fetchall()
    

    #rows = db.engine.execute(sql)    

    # output is the main content, row_output is the content from each record returned
    response_dict = dict()
    response_dict["type"] = "StatsCollection"
    response_dict["classes"] = num_classes

    feature_array = list()

    # For each row returned assemble a dictionary
    for row in rows:
        feature_dict = dict(row)
        feature_dict["id"] = feature_dict["id"].lower()
        feature_dict["table"] = feature_dict["table"].lower()

        # # get ranges of stat values per boundary type
        # for boundary in boundary_names:
        #     boundary_table = "{0}.{1}".format(settings["web_schema"], boundary["name"])
        #
        #     data_table = "{0}.{1}_{2}".format(settings["data_schema"], boundary["name"], feature_dict["table"])
        #
        #     # get the values for the map classes
        #     with get_db_cursor() as pg_cur:
        #         if feature_dict["maptype"] == "values":
        #             stat_field = "tab.{0}" \
        #                 .format(feature_dict["id"], )
        #         else:  # feature_dict["maptype"] == "percent"
        #             stat_field = "CASE WHEN bdy.population > 0 THEN tab.{0} / bdy.population * 100.0 ELSE 0 END" \
        #                 .format(feature_dict["id"], )
        #
        #         # get range of stat values
        #         # feature_dict[boundary_name] = utils.get_equal_interval_bins(
        #         # feature_dict[boundary["name"]] = utils.get_kmeans_bins(
        #         feature_dict[boundary["name"]] = utils.get_min_max(
        #             data_table, boundary_table, stat_field, num_classes, boundary["min"], feature_dict["maptype"],
        #             pg_cur, settings)

        # add dict to output array of metadata
        feature_array.append(feature_dict)

    response_dict["stats"] = feature_array
    # output_array.append(output_dict)

    # print("Got metadata for {0} in {1}".format(boundary_name, datetime.now() - start_time))

    # # Assemble the JSON
    # response_dict["boundaries"] = output_array

    print("Returned metadata in {0}".format(datetime.now() - full_start_time))

    return Response(json.dumps(response_dict), mimetype='application/json')


@main.route("/get-data")
def get_data():

    full_start_time = datetime.now()
    # start_time = datetime.now()

    # # Get parameters from querystring
    # census_year = request.args.get('c')

    map_left = request.args.get('ml')
    map_bottom = request.args.get('mb')
    map_right = request.args.get('mr')
    map_top = request.args.get('mt')

    stat_id = request.args.get('s')
    table_id = request.args.get('t')
    boundary_name = request.args.get('b')
    zoom_level = int(request.args.get('z'))
    InputSSC = request.args.get('InputSSC')
    #print("==>main/views.py::get_data: enter InputSSC="+InputSSC)

    # TODO: add support for equations

    # get the boundary table name from zoom level
    if boundary_name is None:
        boundary_name, min_val = get_boundary(zoom_level)

    display_zoom = str(zoom_level).zfill(2)
    #print("==>main/views.py::get_data: enter line 361")
    with get_db_cursor() as pg_cur:
        # print("Connected to database in {0}".format(datetime.now() - start_time))
        # start_time = datetime.now()

        # build SQL with SQL injection protection
        # yes, this is ridiculous - if someone can find a shorthand way of doing this then fire up the pull requests!
        '''
        sql_template = "SELECT bdy.id, bdy.name, bdy.population, tab.%s / bdy.area AS density, " \
              "CASE WHEN bdy.population > 0 THEN tab.%s / bdy.population * 100.0 ELSE 0 END AS percent, " \
              "tab.%s, geojson_%s AS geometry " \
              "FROM {0}.%s AS bdy " \
              "INNER JOIN {1}.%s_%s AS tab ON bdy.id = tab.{2} " \
              "WHERE bdy.geom && ST_MakeEnvelope(%s, %s, %s, %s, 4283)" \
              .format(settings['web_schema'], settings['data_schema'], settings['region_id_field'])

        sql = pg_cur.mogrify(sql_template, (AsIs(stat_id), AsIs(stat_id), AsIs(stat_id), AsIs(display_zoom),
                                            AsIs(boundary_name), AsIs(boundary_name), AsIs(table_id), AsIs(map_left),
                                            AsIs(map_bottom), AsIs(map_right), AsIs(map_top)))
        '''
        #print("==>main/views.py::get_data: enter line 381")
        sql_template = "SELECT bdy.id, bdy.name, bdy.population, tab.%s / bdy.area AS density, " \
              "CASE WHEN bdy.population > 0 THEN tab.%s / bdy.population * 100.0 ELSE 0 END AS percent, " \
              "tab.%s, geojson_%s AS geometry " \
              "FROM {0}.%s AS bdy " \
              "INNER JOIN {1}.%s_%s AS tab ON bdy.id = tab.{2} " \
              "WHERE bdy.id = '%s'" \
              .format(settings['web_schema'], settings['data_schema'], settings['region_id_field'])
        #print("==>main/views.py::get_data: enter line 389")

        sql = pg_cur.mogrify(sql_template, (AsIs(stat_id), AsIs(stat_id), AsIs(stat_id), AsIs(display_zoom),
                                            AsIs(boundary_name), AsIs(boundary_name), AsIs(table_id), AsIs(InputSSC)))

        print("views.py::get_data: ",end=' ')
        print(sql)
        try:
            pg_cur.execute(sql)
        except psycopg2.Error:
            return "I can't SELECT:<br/><br/>" + str(sql)

        # Retrieve the results of the query
        rows = pg_cur.fetchall()

        # Get the column names returned
        col_names = [desc[0] for desc in pg_cur.description]

    # print("Got records from Postgres in {0}".format(datetime.now() - start_time))
    # start_time = datetime.now()

    # output is the main content, row_output is the content from each record returned
    output_dict = dict()
    output_dict["type"] = "FeatureCollection"

    i = 0
    feature_array = list()

    # For each row returned...
    for row in rows:
        feature_dict = dict()
        feature_dict["type"] = "Feature"

        properties_dict = dict()

        # For each field returned, assemble the feature and properties dictionaries
        for col in col_names:
            if col == 'geometry':
                feature_dict["geometry"] = ast.literal_eval(str(row[col]))
            elif col == 'id':
                feature_dict["id"] = row[col]
            else:
                properties_dict[col] = row[col]

        feature_dict["properties"] = properties_dict

        feature_array.append(feature_dict)

        # start over
        i += 1

    # Assemble the GeoJSON
    output_dict["features"] = feature_array

    # print("Parsed records into JSON in {1}".format(i, datetime.now() - start_time))
    print("get-data: returned {0} records  {1}".format(i, datetime.now() - full_start_time))

    return Response(json.dumps(output_dict), mimetype='application/json')

@main.route("/index2")
def homepage():
    return render_template('index.html')

#########################################
## The above codes are for maps
#########################################