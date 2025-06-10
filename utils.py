import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance between two points on the Earth's surface.
    
    :param lat1: Latitude of the first point in degrees
    :param lon1: Longitude of the first point in degrees
    :param lat2: Latitude of the second point in degrees
    :param lon2: Longitude of the second point in degrees
    :return: Distance between the two points in meters
    """
    R = 6371000  # Radius of the Earth in meters
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def calculate_north_east(lat, lon, center_lat, center_lon):
    """
    Calculate the north and east position relative to a center point.
    
    :param lat: Latitude of the point in degrees
    :param lon: Longitude of the point in degrees
    :param center_lat: Latitude of the center point in degrees
    :param center_lon: Longitude of the center point in degrees
    :return: A tuple (north, east) representing the north and east displacement in meters
    """
    # Calculate the distance in the north-south direction
    north_distance = haversine(center_lat, center_lon, lat, center_lon)
    if lat < center_lat:
        north_distance = -north_distance

    # Calculate the distance in the east-west direction
    east_distance = haversine(center_lat, center_lon, center_lat, lon)
    if lon < center_lon:
        east_distance = -east_distance

    return north_distance, east_distance

def map_range(x, a1, a2, b1, b2):
    """
    Maps a value x from range [a1, a2] to range [b1, b2].
    
    :param x: The value to map.
    :param a1: The lower bound of the input range.
    :param a2: The upper bound of the input range.
    :param b1: The lower bound of the output range.
    :param b2: The upper bound of the output range.
    :return: The mapped value.
    """
    return b1 + (x - a1) * (b2 - b1) / (a2 - a1)