import math

def latlon_distance_finder(lat1,lon1,lat2,lon2):

    earth_radius = 6371.0

    #Converting lat and lon from degrees to radians
    lat1 = math.radians(lat1)
    lon1 = math.radians(lon1)
    lat2 = math.radians(lat2)
    lon2 = math.radians(lon2)

    dist_lon = lon2 - lon1
    dist_lat = lat2 - lat1
    x = math.sin(dist_lat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dist_lon/2)**2
    y = 2 * math.atan2(math.sqrt(x), math.sqrt(1-x))
    distance = earth_radius * y

    return distance

