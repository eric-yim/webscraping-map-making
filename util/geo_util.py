import requests
from urllib.parse import quote
class OSMPlace:
    def __init__(self,info):
        self.location = [info['lat'], info['lon']]
        



class OpenStreetMap:

    @staticmethod
    def get_location_from_address(address):
        params = {
            "q": address,
            "format":"json"
        }
        response = requests.get("https://nominatim.openstreetmap.org/search", params=params)
        info = response.json()[0]

        osmPlace = OSMPlace(info)
        return osmPlace.location

    