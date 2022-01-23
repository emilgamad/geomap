

class MapFilter:
    def __init__(self,data):
        self.index = data.get('index')
        self.farmer_id=data.get('farmer_id')
        self.region_id=data.get('region_id')
        self.province_id=data.get('province_id')
        self.municipality_id=data.get('municipality_id')
        self.barangay_id=data.get('barangay_id')
        self.seed_type=data.get('seed_type')

    def parse_map_filter(self):
        initial_query = "Select * from gpx_info where "
        conditions = []
        if self.index:
            conditions.append("id='{}'".format(self.index))
        if self.farmer_id:
            conditions.append("farmer_id='{}'".format(self.farmer_id))
        if self.province_id:
            conditions.append("province_id='{}'".format(self.province_id))
        if self.municipality_id:
            conditions.append("municipality_id='{}'".format(self.municipality_id))
        if self.barangay_id:
            conditions.append("region_id='{}'".format(self.barangay_id))
        if self.seed_type:
            conditions.append("region_id='{}'".format(self.seed_type))
        sql_string = initial_query+" AND ".join(conditions)
        return sql_string





