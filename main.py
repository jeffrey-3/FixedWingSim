from sim import Simulator
from visuals import Visuals
import threading
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

def sim_loop(visuals):
    sim = Simulator()

    center_lat = sim.get_fdm()['position/lat-geod-deg']
    center_lon = sim.get_fdm()['position/long-gc-deg']

    while True:
        north, east = calculate_north_east(sim.get_fdm()['position/lat-geod-deg'],
                                           sim.get_fdm()['position/long-gc-deg'],
                                           center_lat,
                                           center_lon)

        sim.run()
        visuals.update_flight_state(sim.get_fdm()['attitude/phi-deg'], 
                                    sim.get_fdm()['attitude/theta-deg'], 
                                    sim.get_fdm()['attitude/psi-deg'], 
                                    north, 
                                    east, 
                                    -sim.get_fdm()['position/h-sl-ft'] * 0.3048)

vis = Visuals()

sim_thread = threading.Thread(target=sim_loop, args=(vis,))
sim_thread.daemon = True
sim_thread.start()

vis.run()