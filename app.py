
from flask import Flask, request, jsonify, render_template, request, session
from flask_wtf import FlaskForm
from numpy import conj
from wtforms.fields.choices import SelectField
import connect_to_mysql as con, create_map_markers, create_data_frame, create_map_polygon
import warnings
warnings.filterwarnings("ignore")



app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

#-----------------RCM Database---------------------#
@app.route("/get_map_markers_by_gpx_id_rcm")
def get_map_markers_by_gpx_id():
        rows = con.get_geo_data()
        dataframe = create_data_frame.create_data_frame(rows)
        map = create_map_markers.create_map_marker(dataframe)
        return map._repr_html_()

@app.route("/get_map_polygon_by_gpx_id_rcm")
def get_map_polygon_by_gpx_id():
        rows = con.get_geo_data()
        dataframe = create_data_frame.create_data_frame(rows)
        map = create_map_polygon.create_map_polygon(dataframe)
        return map._repr_html_()

@app.route("/get_all_map_polygon_by_gpx_id_rcm")
def get_all_map_polygon_by_gpx_id():
        rows = con.get_all_geo_data()
        dataframe = create_data_frame.create_data_frame_polygon_from_list(rows)
        map = create_map_polygon.create_map_polygons(dataframe)
        return map._repr_html_()

@app.route("/get_all_map_centroids_from_gpx_infos_rcm")
def get_all_map_centroids_from_gpx_infos():
        rows = con.get_all_gpx_info()
        dataframe = create_data_frame.create_data_frame_for_gpx_info(rows)
        map = create_map_markers.create_map_markers(dataframe)
        return map._repr_html_()


#------------------iFarm Datbase-------------------------#
@app.route("/get_all_map_markers_by_gpx_id_iFarm")
def get_all_map_markers_by_gpx_id_ifarm():
        rows = con.get_all_gpx_info_ifarm()
        dataframe = create_data_frame.create_data_frame_ifarm(rows)
        map = create_map_markers.create_map_markers_ifarm(dataframe)
        return map._repr_html_()

@app.route("/get_map_markers_by_gpx_id_iFarm")
def get_map_markers_by_gpx_id_ifarm():
        data = request.json
        try:
                gpx_id = data.get("gpx_id",None)
        except:
                return "<p>No Gpx Id</p>"  
        rows = con.get_all_gpx_info_by_gpx_id_ifarm(gpx_id)
        dataframe = create_data_frame.create_data_frame_ifarm(rows)
        map = create_map_markers.create_map_marker(dataframe)
        return map._repr_html_()


#-----------------iFarm Dashboard-------------------------#
class Form(FlaskForm):
        choices = ["Choice"]
        region = SelectField('region', choices=con.get_region_rcm())
        province = SelectField('province', choices=[])
        municipality = SelectField('municipality', choices=[])
        barangay = SelectField('barangay', choices=[])
        # crop = SelectField('crop', choices=[])

@app.route("/", methods = ['GET','POST'])
def filter_map():
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
        data = con.get_intervention_data_by_gpx_id(gpx_id)
        return render_template("fields.html",data=data,gpx_id=gpx_id)

@app.route("/filter_basic_map", methods = ['GET','POST'])
def filter_basic_map():
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
        provinces = list(con.get_province_rcm(region = region))
        return jsonify({'provinces':provinces})

@app.route("/municipalities/<province>")
def municipality(province):
        municipality = list(con.get_municipality_rcm(province = province))
        return jsonify({'municipality':municipality})

@app.route("/barangays/<municipality>")
def barangay(municipality):
        barangay = list(con.get_barangay_rcm(municipality = municipality))
        print("munic {}".format(municipality))
        return jsonify({'barangay':barangay})




















def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    
@app.get('/shutdown')
def shutdown():
    shutdown_server()
    return 'Server shutting down..'
