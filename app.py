
from flask import Flask, request, jsonify, render_template, request, session
from flask_wtf import FlaskForm
from numpy import conj
from wtforms.fields.choices import SelectField
import connect_to_mysql as con, create_map_markers, create_data_frame, create_map_polygon, create_reports
import warnings
warnings.filterwarnings("ignore")



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

#-----------------RCM Database---------------------#
@app.route("/get_map_markers_by_gpx_id_rcm")
def get_map_markers_by_gpx_id():
    """
    Returns map markers for a specific GPX ID from the RCM database.
    """
    rows = con.get_geo_data()
    dataframe = create_data_frame.create_data_frame(rows)
    map = create_map_markers.create_map_marker(dataframe)
    return map._repr_html_()

@app.route("/get_map_polygon_by_gpx_id_rcm")
def get_map_polygon_by_gpx_id():
    """
    Returns map polygon for a specific GPX ID from the RCM database.
    """
    rows = con.get_geo_data1()
    dataframe = create_data_frame.create_data_frame(rows)
    map = create_map_polygon.create_map_polygon(dataframe)
    return map._repr_html_()

@app.route("/get_all_map_polygon_by_gpx_id_rcm")
def get_all_map_polygon_by_gpx_id():
    """
    Returns all map polygons by GPX ID from the RCM database.
    """
    rows = con.get_all_geo_data()
    dataframe = create_data_frame.create_data_frame_polygon_from_list(rows)
    map = create_map_polygon.create_map_polygons(dataframe)
    return map._repr_html_()

@app.route("/get_all_map_centroids_from_gpx_infos_rcm")
def get_all_map_centroids_from_gpx_infos():
    """
    Returns all map centroids from GPX infos in the RCM database.
    """
    rows = con.get_all_gpx_info()
    dataframe = create_data_frame.create_data_frame_for_gpx_info(rows)
    map = create_map_markers.create_map_markers(dataframe)
    return map._repr_html_()


#------------------iFarm Datbase-------------------------#
@app.route("/get_all_map_markers_by_gpx_id_iFarm")
def get_all_map_markers_by_gpx_id_ifarm():
    """
    Returns all map markers by GPX ID from the iFarm database.
    """
    rows = con.get_all_gpx_info_ifarm()
    dataframe = create_data_frame.create_data_frame_ifarm(rows)
    map = create_map_markers.create_map_markers_ifarm(dataframe)
    return map._repr_html_()

@app.route("/get_map_markers_by_gpx_id_iFarm")
def get_map_markers_by_gpx_id_ifarm():
    """
    Returns map markers for a specific GPX ID from the iFarm database.
    """
    #data = request.json
    # try:
    #         gpx_id = data.get("gpx_id",None)
    # except:
    #         return "<p>No Gpx Id</p>"  
    rows = con.get_all_gpx_info_by_gpx_id_ifarm("2314-00771-01")
    dataframe = create_data_frame.create_data_frame_ifarm(rows)
    map = create_map_markers.create_map_marker(dataframe)
    return map._repr_html_()


#-----------------iFarm Dashboard-------------------------#
class Form(FlaskForm):
    """
    WTForms form for filtering map data by region, province, municipality, and barangay.
    """
    choices = ["Choice"]
    region = SelectField('region', choices=con.get_region_rcm())
    province = SelectField('province', choices=[])
    municipality = SelectField('municipality', choices=[])
    barangay = SelectField('barangay', choices=[])
    # crop = SelectField('crop', choices=[])

@app.route("/", methods = ['GET','POST'])
def filter_map():
    """
    Renders and processes the main map filter form for iFarm dashboard.
    """
    form = Form()
    form.province.choices = []
    form.municipality.choices = []
    form.barangay.choices = []

    if request.method == 'POST':
        region = request.form.get('region', None)
        province = request.form.get('province', None)
        municipality = request.form.get('municipality', None)
        barangay = request.form.get('barangay', None)

        session['region'] = region
        session['province'] = province
        session['municipality'] = municipality
        session['barangay'] = barangay

        rows = con.get_filter_data(region, province, municipality, barangay)
        if len(rows) == 0:
            return "<p>No Data</p>"
        map = create_map_polygon.add_track_segments(rows)
        map.save("templates/map.html")
    else:
        map = create_map_markers.create_map_markers_ifarm(None)
        map.save("templates/map.html")

    return render_template("filter_map.html",form=form)

@app.route("/fields/<gpx_id>", methods = ['GET'])
def fields(gpx_id):
    """
    Renders the field history for a given GPX ID.
    """
    #data = con.get_intervention_data_by_gpx_id(gpx_id)
    data = con.get_field_history_data_by_gpx_id(gpx_id)
    return render_template("fields.html",data=data,gpx_id=gpx_id,)

@app.route("/filter_basic_map", methods = ['GET','POST'])
def filter_basic_map():
    """
    Renders and processes a basic map filter form for iFarm dashboard.
    """
    form = Form()
    form.province.choices = []
    form.municipality.choices = []
    form.barangay.choices = []
    if request.method == 'POST':
        region = request.form.get('region', None)
        province = request.form.get('province', None)
        municipality = request.form.get('municipality', None)
        barangay = request.form.get('barangay', None)

        rows = con.get_filter_data(region, province, municipality, barangay)
        if len(rows) == 0:
            return "<p>No Data</p>"
        dataframe = create_data_frame.create_filtered_data_frame_ifarm(rows)
        map = create_map_markers.create_map_markers_ifarm(dataframe)
        #map = create_map_polygon.add_track_segments(map,rows)
        map.save("templates/map.html")

    return render_template("filter_map.html",form=form)

@app.route("/provinces/<region>")
def province(region):
    """
    Returns a list of provinces for a given region.
    """
    provinces = list(con.get_province_rcm(region = region))
    return jsonify({'provinces':provinces})

@app.route("/municipalities/<province>")
def municipality(province):
    """
    Returns a list of municipalities for a given province.
    """
    municipality = list(con.get_municipality_rcm(province = province))
    return jsonify({'municipality':municipality})

@app.route("/barangays/<municipality>")
def barangay(municipality):
    """
    Returns a list of barangays for a given municipality.
    """
    barangay = list(con.get_barangay_rcm(municipality = municipality))
    print("munic {}".format(municipality))
    return jsonify({'barangay':barangay})


@app.route("/reports", methods = ['GET','POST'])
def filter_reports():
    """
    Renders and processes the reports filter form and displays report graphs.
    """
    form = Form()
    form.province.choices = []
    form.municipality.choices = []
    form.barangay.choices = []

    if request.method == 'POST':
        region = request.form.get('region', None)
        province = request.form.get('province', None)
        municipality = request.form.get('municipality', None)
        barangay = request.form.get('barangay', None)

        session['region'] = region
        session['province'] = province
        session['municipality'] = municipality
        session['barangay'] = barangay

        rows = con.get_filter_reports(region, province, municipality, barangay)
        if len(rows) == 0:
            return "<p>No Data</p>"

        data_frame = create_data_frame.create_report_data_frame(rows['rows'])
        report = create_reports.graph(
            dataframe=data_frame,
            region = rows.get("region",None),
            province = rows.get("province",None),
            municipality = rows.get("municipality",None),
            barangay = rows.get("barangay",None) 
        )
        #print(report)
        return render_template("filter_reports.html",graphJSON=report,form=form)
    return render_template("filter_reports.html",form=form)



















def shutdown_server():
    """
    Shuts down the Flask development server.
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.get('/shutdown')
def shutdown():
    """
    Endpoint to trigger server shutdown.
    """
    shutdown_server()
    return 'Server shutting down..'
