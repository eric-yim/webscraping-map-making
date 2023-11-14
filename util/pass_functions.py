import math
"""
pass functions
    have a function called check
    return True when want to plot yes

"""
class WithinDistance:
    def __init__(self, map_center, filter_dist):
        self.map_center = map_center
        self.filter_dist = filter_dist
    def check(self, location):
        return is_near(self.map_center, location, self.filter_dist)

class NotWithinDistance:
    def __init__(self, map_centers, filter_dist):
        self.map_centers = map_centers
        self.filter_dist = filter_dist
    def check(self, location):
        for map_center in self.map_centers:
            if is_near(map_center, location, self.filter_dist):
                return False
        return True

def is_near(point0, point1, filter_dist):
    return MathUtil.haversine(*point0, *point1) < filter_dist

class MathUtil:
    # lat lon to km distance
    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        # Radius of the Earth in kilometers
        R = 6371.0

        # Convert latitude and longitude from degrees to radians
        lat1 = math.radians(float(lat1))
        lon1 = math.radians(float(lon1))
        lat2 = math.radians(float(lat2))
        lon2 = math.radians(float(lon2))

        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c

        return distance
