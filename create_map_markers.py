import folium, connect_to_mysql as get_sql
from shapely.geometry import Polygon


def create_map_marker(dataframe):

    map = folium.Map(location = [dataframe.iloc[0]['lat'],dataframe.iloc[0]['lon']], tiles='OpenStreetMap', zoom_start = 18)

    # add marker one by one on the map
    for i in range(0,len(dataframe)):
        folium.Marker(
            location=[dataframe.iloc[i]['lat'], dataframe.iloc[i]['lon']],
            popup=dataframe.iloc[i]['gpx_id'],
        ).add_to(map)

    return map

def create_map_markers(dataframe):
    map = folium.Map(location = [dataframe.iloc[0]['lat'],dataframe.iloc[0]['lon']], tiles='OpenStreetMap', zoom_start = 10)
    # add marker one by one on the map
    for i in range(0,len(dataframe)):
        
        folium.Marker(
            location=[dataframe.iloc[i]['lat'], dataframe.iloc[i]['lon']],
            popup=folium.Popup("gpx_id: {}\r\nArea: {}".format(dataframe.iloc[i]['gpx_id'],dataframe.iloc[i]['area']), parse_html=True, max_width=100)
        ).add_to(map)

    return map

def create_map_markers_ifarm(dataframe):
    try:
        lat = dataframe.iloc[0]['lat']
        long = dataframe.iloc[0]['lon']
    except:
        map = folium.Map(location = [12.8797, 121.7740], tiles='OpenStreetMap', zoom_start=6)
        return map
    
    map = folium.Map(location = [lat,long], tiles='OpenStreetMap',zoom_start=15)

    # add marker one by one on the map
    for i in range(0,len(dataframe)):
        field_id = dataframe.iloc[i]['field_id']
        farmer_id = dataframe.iloc[i]['farmer_id']
        rsbsa_id = dataframe.iloc[i]['rsbsa_id']
        field_name = dataframe.iloc[i]['field_name']
        field_size = dataframe.iloc[i]['field_size']
        gpx_id = dataframe.iloc[i]['gpx_id']
        area = dataframe.iloc[i]['area']
        marker_lat = dataframe.iloc[i]['lat']
        marker_long = dataframe.iloc[i]['lon']
        date_planted = dataframe.iloc[i]['date_planted']
        crop = dataframe.iloc[i]['crop']
        seed_type = dataframe.iloc[i]['seed_type']
        seed_source = dataframe.iloc[i]['seed_source']


        html = """
            <p>field_id: {}<p>
            <p>farmer_id: {}<p>
            <p>rsbsa_id: {}<p>
            <p>field_name: {}<p>
            <p>field_size: {}<p>
            <p>gpx_id: {}</p>
            <p>area: {}</p>
            <p>crop: {}</p>
            <p>date planted: {}</p>
            <p>seed type: {}</p>
            <p>seed source: {}</p> 
            <p>intervention:</p>
            <table border="1">
                <tr>
                    <th>GPX ID</th>
                    <th>Rehab Interview</th>
                    <th>Crop</th>
                    <th>Seed Type</th>
                    <th>Seed Program</th>
                    <th>Unit</th>
                    <th>Rehab Quantity</th>
                    <th>Rehab Amount</th>
                    <th>Damage</th>
                    <th>Damage Date</th>
                </tr>
        """.format(
            field_id,
            farmer_id,
            rsbsa_id,
            field_name,
            field_size,
            gpx_id,
            area,
            crop,
            date_planted,
            seed_type,
            seed_source,None,None)
        
        if gpx_id:
            intervention_data = get_sql.get_intervention_data_by_gpx_id(gpx_id)

        
            if intervention_data:
                intervention_html = """"""
                for i in intervention_data:
                    intervention_html += """
                                            <tr>
                                                <td>{}</td>
                                                <td>{}</td>
                                                <td>{}</td>
                                                <td>{}</td>
                                                <td>{}</td>
                                                <td>{}</td>
                                                <td>{}</td>
                                                <td>{}</td>
                                                <td>{}</td>
                                                <td>{}</td>
                                            </tr>
                                        """.format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9])

                html += intervention_html
                html += """</table>"""                               
        iframe = folium.IFrame(html,width=700,height=600)
        popup = folium.Popup(iframe,parse_html=True,max_width=700)

        folium.Marker(
            location=[marker_lat, marker_long],
            popup=popup
        ).add_to(map)

    return map


