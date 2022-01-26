from numpy import float64
import pandas as pd

def create_data_frame(data):
    gpx_id = []
    longitude = []
    latitude = []

    for i in data:
        gpx_id.append(i[1])
        latitude.append(float(i[2]))
        longitude.append(float(i[3]))

    dataframe = pd.DataFrame({
        'gpx_id':gpx_id,
        'lon':longitude,
        'lat':latitude,
    })

    return dataframe

def create_data_frame_ifarm(data):
    gpx_id = []
    longitude = []
    latitude = []
    area = []
    user = []

    for i in data:
        gpx_id.append(i[1])
        area.append(i[2])
        latitude.append(float(i[3]))
        longitude.append(float(i[4]))
        user.append(i[5])
        

    dataframe = pd.DataFrame({
        'gpx_id':gpx_id,
        'area': area,
        'lon':longitude,
        'lat':latitude,
        'user':user 

    })

    return dataframe


def create_data_frame_polygon_from_list(data):
    dataframeList = []
    df = create_data_frame(data)
    gpx_id = set(df['gpx_id'])
    for i in gpx_id:
        plot = df[df['gpx_id']==i]
        dataframeList.append(plot)

    return dataframeList

def create_data_frame_for_gpx_info(data):
    gpx_id = []
    longitude = []
    latitude = []
    area = []

    for i in data:
        gpx_id.append(i[1])
        area.append(float(i[2]))
        latitude.append(float(i[3]))
        longitude.append(float(i[4]))

    dataframe = pd.DataFrame({
        'gpx_id':gpx_id,
        'area':area,
        'lon':longitude,
        'lat':latitude,
    })

    return dataframe


def create_filtered_data_frame_ifarm(data):
    gpx_id = []
    longitude = []
    latitude = []
    area = []
    field_name = []
    field_id = []
    farmer_id = []
    rsbsa_id = []
    field_size = []
    date_planted = []
    crop = []
    seed_type = []
    seed_source = []
    intervention = []


    for i in data:
        if i[7] and i[8]: 
            field_id.append(i[0])
            farmer_id.append(i[1])
            rsbsa_id.append(i[2])
            field_name.append(i[3])
            field_size.append(i[4])
            gpx_id.append(i[5])
            area.append(i[6])
            latitude.append(float(i[7]))
            longitude.append(float(i[8]))
            date_planted.append(i[9])
            crop.append(i[10])
            seed_type.append(i[11])
            seed_source.append(i[12])

        else:
            pass

    dataframe = pd.DataFrame({
        'field_id': field_id,
        'farmer_id': farmer_id,
        'rsbsa_id': rsbsa_id,
        'field_name': field_name,
        'field_size': field_size,
        'gpx_id':gpx_id,
        'area': area,
        'lat':latitude,
        'lon':longitude,
        'date_planted': date_planted,
        'crop': crop,
        'seed_type': seed_type,
        'seed_source': seed_source
    })

    return dataframe

def create_filtered_polygon_dataframe(data):
    id = []
    gpx_id = []
    latitude = []
    longitude = []
    elevation = []
    time_measured = []
    status = []

    #print(data)
    for i in data:
        if i[2] and i[3]: 
            id.append(i[0])
            gpx_id.append(i[1])
            latitude.append(float(i[2]))
            longitude.append(float(i[3]))
        else:
            print(i)
            pass
    
    dataframe = pd.DataFrame({
        'id': id,
        'gpx_id':gpx_id,
        'lat':latitude,
        'lon':longitude
    })

    return dataframe