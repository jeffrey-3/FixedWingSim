import jsbsim
import time
import utils
import math
from queue import Queue
import threading
import geomag
import numpy as np
import navpy
from hardware_interface import ControlInput
from dataclasses import dataclass

@dataclass
class SimulatedSensors:
    ax: float
    ay: float
    az: float
    gx: float
    gy: float
    gz: float
    mx: float
    my: float
    mz: float
    baro_asl: float
    gps_lat: float
    gps_lon: float
    of_x: float
    of_y: float

@dataclass
class VehicleState:
    roll: float
    pitch: float
    yaw: float
    lat: float
    lon: float
    alt: float

class FlightDynamicsModel:
    def __init__(self, initial_lat, initial_lon, control_input_queue: Queue, simulated_sensors_queue: Queue, vehicle_state_queue: Queue):
        self.control_input_queue = control_input_queue
        self.simulated_sensors_queue = simulated_sensors_queue
        self.vehicle_state_queue = vehicle_state_queue

        self.fdm = jsbsim.FGFDMExec("models_jsbsim", None)
        self.fdm.load_model("YardStik")

        self._set_initial_conditions(initial_lat, initial_lon)

        self.fdm.run_ic()
        self.fdm.set_dt(0.008)

        self.start_time = time.time()

        threading.Thread(target=self._update, daemon=True).start()
    
    def _set_initial_conditions(self, initial_lat, initial_lon):
        self.fdm["ic/lat-geod-deg"] = initial_lat
        self.fdm["ic/long-gc-deg"] = initial_lon
        self.fdm["ic/h-sl-ft"] = 5
        self.fdm['attitude/phi-deg'] = 0
        self.fdm['attitude/theta-deg'] = 0
        self.fdm['ic/psi-true-deg'] = 0
        self.fdm["ic/vc-kts"] = 0

    def _update(self):
        if self.control_input_queue.not_empty():
            control_input: ControlInput = self.control_input_queue.get()
            self.fdm['fcs/elevator-cmd-norm'] = control_input.elevator
            self.fdm['fcs/aileron-cmd-norm'] = control_input.rudder
            self.fdm['fcs/throttle-cmd-norm'] = control_input.throttle

        sim_time = self.fdm.get_sim_time()
        real_time = time.time() - self.start_time
        if real_time >= sim_time:
            self.fdm.run()

            mag = self._simulate_mag(
                self.fdm['position/lat-geod-deg'], 
                self.fdm['position/long-gc-deg'], 
                self.fdm['attitude/phi-rad'], 
                self.fdm['attitude/theta-rad'], 
                self.fdm['attitude/psi-rad'] - math.pi
            )
                
            self.simulated_sensors_queue.put(
                SimulatedSensors(
                    self.fdm['accelerations/n-pilot-x-norm'], 
                    self.fdm['accelerations/n-pilot-y-norm'],
                    self.fdm['accelerations/n-pilot-z-norm'],
                    self.fdm['velocities/p-rad_sec'] * 180 / math.pi,
                    self.fdm['velocities/q-rad_sec'] * 180 / math.pi,
                    self.fdm['velocities/r-rad_sec'] * 180 / math.pi,
                    -mag[0],
                    -mag[1],
                    -mag[2],
                    self.fdm['position/h-sl-ft'] * 0.3048,
                    int(self.fdm['position/lat-geod-deg'] * 1e7),
                    int(self.fdm['position/long-gc-deg'] * 1e7),
                    int(0),
                    int(0)
                )
            )

            self.vehicle_state_queue.put(
                VehicleState(
                    self.fdm.get_fdm()['attitude/phi-deg'], 
                    self.fdm.get_fdm()['attitude/theta-deg'], 
                    self.fdm.get_fdm()['attitude/psi-deg'], 
                    self.fdm.get_fdm()['position/lat-geod-deg'],
                    self.fdm.get_fdm()['position/long-gc-deg'],
                    self.fdm.get_fdm()['position/h-sl-ft'] * 0.3048
                )
            )
    
    def _simulate_mag(self, lat_deg, lon_deg, phi_rad, the_rad, psi_rad):
        gm = geomag.geomag.GeoMag()
        mag = gm.GeoMag(lat_deg, lon_deg)
        mag_ned = np.array( [mag.bx, mag.by, mag.bz] )
        norm = np.linalg.norm(mag_ned)
        mag_ned /= norm
        N2B = navpy.angle2dcm(psi_rad, the_rad, phi_rad, input_unit='rad')
        mag_body = N2B.dot(mag_ned)
        norm = np.linalg.norm(mag_body)
        mag_body /= norm
        # print("  mag ned:", mag_ned, "body:", mag_body)
        return mag_body