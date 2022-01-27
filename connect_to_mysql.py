import pymysql

server_host = "127.0.0.1"
user = "root"
password = ""
database = "rasph"
database2 = "farmers"
database3 = "u509806649_ifarm2"


def get_region_rcm():
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    cursor.execute("SELECT region_id,region FROM `tblregion`")
    data = cursor.fetchall()
    return data

def get_province_rcm(region=None):
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    if region:
        cursor.execute("SELECT tblprovince.province_id,tblprovince.province,tblregion.region \
                        FROM tblprovince join tblregion \
                        on tblprovince.region_id = tblregion.region_id \
                        where tblregion.region_id = '{}'".format(region))
    else:
        cursor.execute("SELECT province_id,province FROM `tblprovince`")
    data = cursor.fetchall()
    return data

def get_municipality_rcm(province=None):
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    if province:
        cursor.execute("SELECT tblmunicipality.municipality_id,tblmunicipality.municipality,tblprovince.province \
                        FROM tblmunicipality join tblprovince \
                        on tblprovince.province_id = tblmunicipality.province_id \
                        where tblprovince.province_id = '{}'".format(province))
    else:
        cursor.execute("SELECT municipality_id,municipality FROM `tblmunicipality`")
    data = cursor.fetchall()
    return data

def get_barangay_rcm(municipality=None):
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    if municipality:
        cursor.execute("SELECT tblbarangay.barangay_id,tblbarangay.barangay,tblmunicipality.municipality \
                        FROM tblbarangay join tblmunicipality \
                        on tblmunicipality.municipality_id = tblbarangay.municipality_id \
                        where tblmunicipality.municipality_id = '{}'".format(municipality))
    else:
        cursor.execute("SELECT barangay_id,barangay FROM `tblbarangay`")
    data = cursor.fetchall()
    return data

# def get_crop_rcm():
#     connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
#     cursor = connection.cursor()
#     cursor.execute("SELECT variety_id, variety_name ")
#     data = cursor.fetchall()
#     rows = []
#     data = cursor.fetchall()
#     rows = []
#     for d in data:
#         rows.append((d[0],d[1]))
#     return rows


def get_geo_data1():
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    #connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    cursor.execute("Select * from gpx_track_segments where gpx_id='2314-00771-01'")
    #cursor.execute("Select * from gpx_infos where user='2036'")
    rows = cursor.fetchall()
    
    return rows

def get_geo_data(gpx_id):
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    statement = "Select * from gpx_track_segments where gpx_id = '{}'".format(gpx_id)
    #print(statement)
    cursor.execute(statement)
    rows = cursor.fetchall()
    return rows

def get_filter_data(region, province, municipality, barangay):
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    query_string = ("SELECT fields.field_id,fields.farmer_id,farmers.rsbsa_id,fields.field_name,fields.field_size_ha,fields.gpx_id, gpx_infos.area, gpx_infos.center_lat, gpx_infos.center_lng, tblplant.dtmPlantPlanted, tblrefcom.strCom, tblrefseedtype.strSeedType, tblrefseedsrc.strSeedSrc FROM fields LEFT JOIN farmers ON farmers.farmer_id = fields.farmer_id LEFT JOIN gpx_infos ON gpx_infos.gpx_id = fields.gpx_id  LEFT JOIN tblplant ON tblplant.strPlantGpxId = fields.gpx_id LEFT JOIN tblrefcom ON tblplant.intPlantComId =  tblrefcom.intComId LEFT JOIN tblrefseedtype ON tblplant.intPlantSeedTypeId LEFT JOIN tblrefseedsrc ON tblrefseedsrc.intSeedSrcID =  tblplant.intPlantSeedSrcId WHERE ")
    if region:
        condition_string = "farmers.region_id = {}".format(region)
    if province:
        condition_string = "farmers.province_id = {}".format(province)
    if municipality:
        condition_string = "farmers.municipality_id = {}".format(municipality)
    if barangay:
        condition_string = "farmers.barangay_id = {}".format(barangay)
    full_string = query_string+condition_string
    #print(full_string)
    cursor.execute(query_string+condition_string)
    rows = cursor.fetchall()
    return rows 

def get_all_geo_data():
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database)
    cursor = connection.cursor()
    cursor.execute("Select * from gpx_track_segments")
    rows = cursor.fetchall()
    
    return rows

def get_all_gpx_info():
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database)
    cursor = connection.cursor()
    cursor.execute("Select * from gpx_infos")
    rows = cursor.fetchall()
    
    return rows

def get_farmer_data(gpx_id):
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database)
    cursor = connection.cursor()
    statement = "Select * from farmers where farmer_id='{}'".format(gpx_id)
    #print(statement)
    cursor.execute("Select * from farmers where farmer_id='{}'".format(gpx_id))
    rows = cursor.fetchall()
    return rows

def get_all_gpx_info_ifarm():
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    cursor.execute("Select * from gpx_infos")
    rows = cursor.fetchall()
    
    return rows

def get_all_gpx_info_by_gpx_id_ifarm(gpx_id):
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    statement = "Select * from gpx_infos where gpx_id='{}'".format(gpx_id)
    #print(statement)
    cursor.execute(statement)
    #cursor.execute("SELECT * FROM farmers join gpx_infos where farmer_id where gpx_id='{}'".format(gpx_id))
    rows = cursor.fetchall()
    return rows

def get_farmer_data_ifarm(farmer_id):
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    statement = "Select * from farmers where farmer_id='{}'".format(farmer_id)
    #print(statement)
    cursor.execute(statement)
    rows = cursor.fetchall()
    return rows

def get_intervention_data_by_gpx_id(gpx_id):
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    statement = "SELECT tblrehab.strRehabGpxId, tblrehab.dtmRehabInterview, tblrefcom.strCom, tblrefseedsrc.strSeedSrc, tblrefprog.strProg, tblrefunit.strUnit, tblrehab.decRehabQty, tblrehab.decRehabAmt, tblrefdmg.strDmg, tblrefdmg.dtmDmg FROM tblrehab LEFT JOIN tblrefcom ON tblrehab.intRehabComId = tblrefcom.intComId LEFT JOIN tblrefseedsrc ON tblrehab.intRehabFundSrcId = tblrefseedsrc.intSeedSrcId LEFT JOIN tblrefprog ON tblrehab.intRehabProgActId = tblrefprog.intProgId LEFT JOIN tblrefunit ON tblrehab.intRehabUnitId = tblrefunit.intUnitId LEFT JOIN tblrefdmg ON tblrehab.intRehabDmgId = tblrefdmg.intDmgId WHERE tblrehab.strRehabGpxId = '{}'".format(gpx_id)
    cursor.execute(statement)
    rows = cursor.fetchall()
    return rows

def get_field_history_data_by_gpx_id(gpx_id):
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    statement = "SELECT tblplant.dtmPlantPlanted,fields.farmer_id,farmers.rsbsa_id, tblrefcom.strCom, tblrefseedtype.strSeedType, tblrefseedsrc.strSeedSrc, tblharvest.decHarvestAvgYield, tblrefdmg.strDmg, tbldmg.dtmDmgOccurrence, tblrefprog.strProg FROM tblplant LEFT JOIN fields ON fields.gpx_id = tblplant.strPlantGpxId LEFT JOIN farmers ON fields.farmer_id = farmers.farmer_id LEFT JOIN tblrefcom ON tblplant.intPlantComId = tblrefcom.intComId LEFT JOIN tblrefseedtype ON tblplant.intPlantSeedTypeId = tblrefseedtype.intSeedTypeId LEFT JOIN tblrefseedsrc ON tblplant.intPlantSeedSrcId = tblrefseedsrc.intSeedSrcId LEFT JOIN tblharvest ON tblplant.intPlantId = tblharvest.intHarvestPlantId LEFT JOIN tbldmg ON tblplant.intPlantId = tbldmg.intDmgPlantId LEFT JOIN tblrefdmg ON tbldmg.intDmgCauseId = tblrefdmg.intDmgId LEFT JOIN tblrehab ON tblplant.intPlantId = tblrehab.intRehabPlantId LEFT JOIN tblrefprog ON tblrehab.intRehabProgActId = tblrefprog.intProgId WHERE gpx_id = '{}'".format(gpx_id)
    cursor.execute(statement)
    rows = cursor.fetchall()
    return rows