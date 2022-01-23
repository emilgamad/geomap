import folium, geopandas as gpd, connect_to_mysql as get_sql, create_data_frame, create_map_markers
from shapely import geometry
from shapely.geometry import Polygon
from flask import url_for

def create_map_polygon(dataframe):

    coordi = zip(dataframe['lon'],dataframe['lat'],)
    polygon_geom = Polygon(coordi)
    polygon = gpd.GeoDataFrame(index=[0],crs={'init':'epsg:4326'}, geometry=[polygon_geom])

    map = folium.Map(location = [dataframe.iloc[0]['lat'],dataframe.iloc[0]['lon']], tiles='OpenStreetMap', zoom_start = 18)
    folium.GeoJson(polygon).add_to(map)
    folium.LatLngPopup().add_to(map)
    return map

def create_map_polygons(dataframeList:list): 
    map = folium.Map(location = [dataframeList[0].iloc[0]['lat'],dataframeList[0].iloc[0]['lon']], tiles='OpenStreetMap', zoom_start = 16)
    
    for i in dataframeList:
        coordi = zip(i['lon'],i['lat'],)
        polygon_geom = Polygon(coordi)
        polygon = gpd.GeoDataFrame(index=[0],crs={'init':'epsg:4326'}, geometry=[polygon_geom])
        map_polygon = folium.GeoJson(polygon)

        gpx_id = i.iloc[0]['gpx_id']
        farmer_info = get_sql.get_farmer_data(gpx_id)
        if farmer_info:
            area = None 
            farmer = "{} {}".format(farmer_info[0][3],farmer_info[0][6])
        html = """
            <p>gpx_id:{}</p>
            <p>farmer: {}</p>
            <p>area: {}</p>
        """.format(gpx_id,farmer,area)
        iframe = folium.IFrame(html,width=200,height=200)
        popup = folium.Popup(iframe,max_width=200)
        map_polygon.add_child(popup)#folium.Popup("gpx_id: {}".format()))
        map.add_child(map_polygon)
    return map

def add_track_segments(rows):
    dataframe = create_data_frame.create_filtered_data_frame_ifarm(rows)
    try:
        lat = dataframe.iloc[0]['lat']
        long = dataframe.iloc[0]['lon']
    except:
        map = folium.Map(location = [12.8797, 121.7740], tiles='OpenStreetMap', zoom_start=6)
        return map
                             
        
    
    map = folium.Map(location = [lat,long], tiles='OpenStreetMap',zoom_start=15)
    for i in rows:
        gpx_id = i[5]
        gpx_track_segments = get_sql.get_geo_data(gpx_id)
        polygon_dataframe = create_data_frame.create_filtered_polygon_dataframe(gpx_track_segments)
        coordi = zip(polygon_dataframe['lon'],polygon_dataframe['lat'])
        polygon_geom = Polygon(coordi)
        details = dataframe.loc[dataframe['gpx_id'] == gpx_id]
        if not details.empty:
            html = """
                <p>farmer_id: {}<p>
                <p>field_id: {}<p>
                <p>field_size: {}<p>
                <p>date planted: {}</p>
                <p>seed type: {}</p>
                <p>seed source: {}</p>   
            """.format(
                details['farmer_id'].values[0],
                details['field_id'].values[0],
                details['field_size'].values[0],
                details['date_planted'].values[0],
                details['seed_type'].values[0],
                details['seed_source'].values[0])
            iframe = folium.IFrame(html,width=250,height=250)
       

        #try:
        
        polygon = gpd.GeoDataFrame(index=[0],crs={'init':'epsg:4326'}, geometry=[polygon_geom])
        folium_polygon = folium.GeoJson(polygon)
        if not details.empty:
            folium.Tooltip(html).add_to(folium_polygon)
            folium.Popup("<p><a href=/fields/{}>Interventions</a></p>".format(gpx_id)).add_to(folium_polygon)
        map.add_child(folium_polygon)

        # except:
        #     pass

        
    return map




        
