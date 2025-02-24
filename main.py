from sim import Simulator
from visuals import Visuals
import threading
from utils import *

def sim_loop(visuals):
    sim = Simulator()

    center_lat = sim.get_fdm()['position/lat-geod-deg']
    center_lon = sim.get_fdm()['position/long-gc-deg']

    while True:
        if visuals.mouse_enable:
            sim.set_controls(visuals.aileron, visuals.elevator, visuals.throttle)
        else:
            sim.set_controls(0, 0, 0)

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