"""Support for coolmap path,estimated_time and estimated distance .

This module provides the path co-ordinate, estimated distance and estimated
time to cover the distance based on there pick-up and delivery latitude and longitude.


Method to get the estimated time:
----------------------------------
<CoolMapRoutePth_Obj>.estimated_time(required_unit='m/h/s')
        
        "m" - Return the estimated time in Minuted
        "h" - Return the estimated time in Hour
        "s" - Reeturn the estimated time in Second

Example:
    Input:

    >><CoolMapRoutePth_Obj>.estimated_time('s')

    Output:

    >>'6656.05 Second'
    
        
Method to get the estimated distance:
----------------------------------
<CoolMapRoutePth_Obj>.estimated_distance(required_unit='m/h/s')
        "m" - REturn the distance time in Miles
        "k" - Return the distance time in Kilometer
        "n" - Reeturn the distance time in Nautical Mile
        "t" - Reeturn the distance time in Meter

Example:
    Input:

    >>CoolMapRoutePth_Obj>.estimated_distance('t')

    Output:

    >>'144062.0 Meter'
        
Method to get_path 
----------------------------------
<CoolMapRoutePth_Obj>.get_path()

Example:
    Input:

    >><CoolMapRoutePth_Obj>.get_path()

    Output:

    >>'38.242287,-76.56314400000001;38.242289,-76.563149;...'
"""
import requests, json, polyline
import urllib.parse
 
class CoolmapRoutePath:
    def __init__(self, from_lat_log,to_lat_log, mapbox_api_key ):
        self.from_lat_log = from_lat_log
        self.to_lat_log = to_lat_log
        self.mapbox_api_key = mapbox_api_key
        #defining as private instance variable
        self.__response = self.__get_response
    
    #defineing a private method
    @property   
    def __get_response(self):
        headers = {'Content-Type': 'application/json', 'Authorization': ''}
        url = "https://api.mapbox.com/valhalla/v1/route/?"
        from_lat,from_lon = self.from_lat_log.split(",")
        to_lat,to_lon  = self.to_lat_log.split(",")
        param = {"locations":[{"lat": float(from_lat),"lon": float(from_lon)},{"lat": to_lat,"lon": to_lon,}],"costing": "truck","costing_options": {"truck": {"height": 3.66,"width": "2.6","length": "21.64","axle_load": "18.07","hazmat": False}}}
        request_params = {'json': json.dumps(param), 'access_token': self.mapbox_api_key}
        request_url = url + urllib.parse.urlencode(request_params)
        return requests.get(request_url, headers=headers).json()

    def estimated_time(self,required_unit="M"):
        required_unit = required_unit.upper()
        unit = {"M":[0.0166667, "Minutes"],"H":[0.000277778,"Hour"], "S":[1,"Second"]}
        return f"{str(round((self.__response['trip']['summary']['time'] * unit.get(required_unit)[0]), 2))} {unit.get(required_unit)[1]}"
    
    def estimated_distance(self,required_unit="M" ):
        required_unit = required_unit.upper()
        unit = {"M":[0.621371, "Miles"],"K":[1,"Kilometer"], "N":[0.539957,"Nautical Mile"], "T":[1000, "Meter"]}
        return f"{str(round(self.__response['trip']['summary']['length'] * unit.get(required_unit)[0], 2))} {unit.get(required_unit)[1]}"
   
    def get_path(self):
        return ";".join([f'{l[0] * 0.1},{l[1] * 0.1}' for l in polyline.decode(self.__response['trip']['legs'][0]["shape"])])