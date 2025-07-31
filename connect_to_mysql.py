import pymysql

server_host = "127.0.0.1"
user = "root"
password = ""
database = "rasph"
database2 = "farmers"
database3 = "u509806649_ifarm2"


def get_region_rcm():
    """
    Fetches all regions from the database.
    Returns:
        list: List of region tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    cursor.execute("SELECT region_id,region FROM `tblregion`")
    data = cursor.fetchall()
    return data

def get_province_rcm(region=None):
    """
    Fetches all provinces, optionally filtered by region.
    Args:
        region (str, optional): Region ID to filter provinces.
    Returns:
        list: List of province tuples.
    """
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
    """
    Fetches all municipalities, optionally filtered by province.
    Args:
        province (str, optional): Province ID to filter municipalities.
    Returns:
        list: List of municipality tuples.
    """
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
    """
    Fetches all barangays, optionally filtered by municipality.
    Args:
        municipality (str, optional): Municipality ID to filter barangays.
    Returns:
        list: List of barangay tuples.
    """
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
    """
    Fetches geo data for a hardcoded GPX ID.
    Returns:
        list: List of geo data tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    #connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    cursor.execute("Select * from gpx_track_segments where gpx_id='2314-00771-01'")
    #cursor.execute("Select * from gpx_infos where user='2036'")
    rows = cursor.fetchall()
    
    return rows

def get_geo_data(gpx_id):
    """
    Fetches geo data for a given GPX ID.
    Args:
        gpx_id (str): GPX ID to fetch data for.
    Returns:
        list: List of geo data tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    statement = "Select * from gpx_track_segments where gpx_id = '{}'".format(gpx_id)
    #print(statement)
    cursor.execute(statement)
    rows = cursor.fetchall()
    return rows

def get_filter_data(region, province, municipality, barangay):
    """
    Fetches filtered data based on region, province, municipality, and barangay.
    Args:
        region, province, municipality, barangay: Filter parameters.
    Returns:
        list: List of filtered data tuples.
    """
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
    """
    Fetches all geo data from the database.
    Returns:
        list: List of geo data tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database)
    cursor = connection.cursor()
    cursor.execute("Select * from gpx_track_segments")
    rows = cursor.fetchall()
    
    return rows

def get_all_gpx_info():
    """
    Fetches all GPX info from the database.
    Returns:
        list: List of GPX info tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database)
    cursor = connection.cursor()
    cursor.execute("Select * from gpx_infos")
    rows = cursor.fetchall()
    
    return rows

def get_farmer_data(gpx_id):
    """
    Fetches farmer data for a given GPX ID.
    Args:
        gpx_id (str): GPX ID to fetch farmer data for.
    Returns:
        list: List of farmer data tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database)
    cursor = connection.cursor()
    statement = "Select * from farmers where farmer_id='{}'".format(gpx_id)
    #print(statement)
    cursor.execute("Select * from farmers where farmer_id='{}'".format(gpx_id))
    rows = cursor.fetchall()
    return rows

def get_all_gpx_info_ifarm():
    """
    Fetches all GPX info from the iFarm database.
    Returns:
        list: List of GPX info tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    cursor.execute("Select * from gpx_infos")
    rows = cursor.fetchall()
    
    return rows

def get_all_gpx_info_by_gpx_id_ifarm(gpx_id):
    """
    Fetches GPX info by GPX ID from the iFarm database.
    Args:
        gpx_id (str): GPX ID to fetch info for.
    Returns:
        list: List of GPX info tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    statement = "Select * from gpx_infos where gpx_id='{}'".format(gpx_id)
    #print(statement)
    cursor.execute(statement)
    #cursor.execute("SELECT * FROM farmers join gpx_infos where farmer_id where gpx_id='{}'".format(gpx_id))
    rows = cursor.fetchall()
    return rows

def get_farmer_data_ifarm(farmer_id):
    """
    Fetches farmer data by farmer ID from the iFarm database.
    Args:
        farmer_id (str): Farmer ID to fetch data for.
    Returns:
        list: List of farmer data tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    statement = "Select * from farmers where farmer_id='{}'".format(farmer_id)
    print(statement)
    cursor.execute(statement)
    rows = cursor.fetchall()
    return rows

def get_intervention_data_by_gpx_id(gpx_id):
    """
    Fetches intervention data by GPX ID from the iFarm database.
    Args:
        gpx_id (str): GPX ID to fetch intervention data for.
    Returns:
        list: List of intervention data tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    statement = "SELECT tblrehab.strRehabGpxId, tblrehab.dtmRehabInterview, tblrefcom.strCom, tblrefseedsrc.strSeedSrc, tblrefprog.strProg, tblrefunit.strUnit, tblrehab.decRehabQty, tblrehab.decRehabAmt, tblrefdmg.strDmg, tblrefdmg.dtmDmg FROM tblrehab LEFT JOIN tblrefcom ON tblrehab.intRehabComId = tblrefcom.intComId LEFT JOIN tblrefseedsrc ON tblrehab.intRehabFundSrcId = tblrefseedsrc.intSeedSrcId LEFT JOIN tblrefprog ON tblrehab.intRehabProgActId = tblrefprog.intProgId LEFT JOIN tblrefunit ON tblrehab.intRehabUnitId = tblrefunit.intUnitId LEFT JOIN tblrefdmg ON tblrehab.intRehabDmgId = tblrefdmg.intDmgId WHERE tblrehab.strRehabGpxId = '{}'".format(gpx_id)
    cursor.execute(statement)
    rows = cursor.fetchall()
    return rows

def get_field_history_data_by_gpx_id(gpx_id):
    """
    Fetches field history data by GPX ID from the iFarm database.
    Args:
        gpx_id (str): GPX ID to fetch field history for.
    Returns:
        list: List of field history data tuples.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    statement = """
    SELECT tblplant.dtmPlantPlanted,
       fields.farmer_id,farmers.rsbsa_id, 
       tblrefcom.strCom, 
       tblrefseedtype.strSeedType, 
       tblrefseedsrc.strSeedSrc, 
       tblharvest.decHarvestAvgYield, 
       tblrefdmg.strDmg, 
       tblrefdmg.dtmDmg, 
       tblrefprog.strProg 
    FROM tblplant LEFT JOIN fields ON fields.gpx_id = tblplant.strPlantGpxId 
                LEFT JOIN farmers ON fields.farmer_id = farmers.farmer_id 
                LEFT JOIN tblrefcom ON tblplant.intPlantComId = tblrefcom.intComId 
                LEFT JOIN tblrefseedtype ON tblplant.intPlantSeedTypeId = tblrefseedtype.intSeedTypeId 
                LEFT JOIN tblrefseedsrc ON tblplant.intPlantSeedSrcId = tblrefseedsrc.intSeedSrcId 
                LEFT JOIN tblharvest ON tblplant.intPlantId = tblharvest.intHarvestPlantId 
                LEFT JOIN tbldmg ON tblplant.intPlantId = tbldmg.intDmgPlantId 
                LEFT JOIN tblrefdmg ON tbldmg.intDmgCauseId = tblrefdmg.intDmgId 
                LEFT JOIN tblrehab ON tblplant.intPlantId = tblrehab.intRehabPlantId 
                LEFT JOIN tblrefprog ON tblrehab.intRehabProgActId = tblrefprog.intProgId 
    WHERE '{}' ORDER BY `tblrefdmg`.`dtmDmg`  ASC""".format(gpx_id)  
    #print(statement)  
    cursor.execute(statement)
    rows = cursor.fetchall()
    return rows

def get_filter_reports(region, province, municipality, barangay):
    """
    Fetches filtered report data based on region, province, municipality, and barangay.
    Args:
        region, province, municipality, barangay: Filter parameters.
    Returns:
        dict: Dictionary containing report data and filter parameters.
    """
    connection = pymysql.connect(host=server_host,user=user,passwd=password,database=database3)
    cursor = connection.cursor()
    query_string = """
    SELECT fields.gpx_id, 
            tblrefcom.strCom,
            tblrefvar.strVar,
            tblrefeco.strEco,
            tblrefseedtype.strSeedType, 
            tblplant.decPlantParcelArea, 
            tblplant.decPlantPlantedArea,
            tblregion.region,
            tblprovince.province,
            tblmunicipality.municipality,
            tblbarangay.barangay
    FROM fields LEFT JOIN tblplant ON fields.gpx_id = tblplant.strPlantGpxId 
                LEFT JOIN tblrefcom ON tblplant.intPlantComId = tblrefcom.intComId 
                LEFT JOIN tblrefseedtype ON tblrefseedtype.intSeedTypeId = tblplant.intPlantSeedTypeId
                LEFT JOIN tblrefvar ON tblrefvar.intVarId = tblplant.intPlantVarId
                LEFT JOIN tblregion ON fields.region_id = tblregion.region_id
                LEFT JOIN tblprovince ON fields.province_id = tblprovince.province_id
                LEFT JOIN tblmunicipality ON fields.municipality_id = tblmunicipality.municipality_id
                LEFT JOIN tblbarangay ON fields.barangay_id = tblbarangay.barangay_id
                LEFT JOIN tblrefeco ON tblplant.intPlantEcoId = tblrefeco.intEcoId    
    WHERE """    
    if region:
        condition_string = "fields.region_id = {}".format(region)
    if province:
        condition_string = "fields.province_id = {}".format(province)
    if municipality:
        condition_string = "fields.municipality_id = {}".format(municipality)
    if barangay:
        condition_string = "fields.barangay_id = {}".format(barangay)
    full_string = query_string+condition_string
    print(full_string)
    #cursor.execute(query_string+condition_string)
    cursor.execute(full_string)
    rows = cursor.fetchall()
    data = {'rows':rows,"region":region,'province':province,'municipality':municipality,'barangay':barangay}
    return data 