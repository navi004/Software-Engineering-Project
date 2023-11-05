import geopy
from geopy.geocoders import Nominatim

def get_lat_long_for_address(address):
    geolocator = Nominatim(user_agent="geoapiExercises")

    try:
        location = geolocator.geocode(address)
        if location:
            latitude = location.latitude
            longitude = location.longitude
            return latitude, longitude
        else:
            return None, None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None
