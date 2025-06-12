import jsbsim
import time
import math
import threading
import geomag
import numpy as np
import navpy
from data_structures import *

class FlightDynamicsModel:
    def __init__(self, initial_lat, initial_lon, control_input: ControlInput, simulated_sensors: SimulatedSensors, vehicle_state: VehicleState):
        self.control_input = control_input
        self.simulated_sensors = simulated_sensors
        self.vehicle_state = vehicle_state

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

    def _update(self):
        while True:
            self.fdm['fcs/elevator-cmd-norm'] = self.control_input.elevator
            self.fdm['fcs/aileron-cmd-norm'] = self.control_input.rudder
            self.fdm['fcs/throttle-cmd-norm'] = max(self.control_input.throttle, 0.00001) # For some reason there is a bug when throttle is 0

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
                    
                self.simulated_sensors.ax = self.fdm['accelerations/n-pilot-x-norm']
                self.simulated_sensors.ay = self.fdm['accelerations/n-pilot-y-norm']
                self.simulated_sensors.az = self.fdm['accelerations/n-pilot-z-norm']
                self.simulated_sensors.gx = self.fdm['velocities/p-rad_sec'] * 180 / math.pi
                self.simulated_sensors.gy = self.fdm['velocities/q-rad_sec'] * 180 / math.pi
                self.simulated_sensors.gz = self.fdm['velocities/r-rad_sec'] * 180 / math.pi
                self.simulated_sensors.mx = -mag[0]
                self.simulated_sensors.my = -mag[1]
                self.simulated_sensors.mz = -mag[2]
                self.simulated_sensors.baro_asl = self.fdm['position/h-sl-ft'] * 0.3048
                self.simulated_sensors.gps_lat = int(self.fdm['position/lat-geod-deg'] * 1e7)
                self.simulated_sensors.gps_lon = int(self.fdm['position/long-gc-deg'] * 1e7)
                self.simulated_sensors.of_x = int(0)
                self.simulated_sensors.of_y = int(0)

                self.vehicle_state.roll = self.fdm['attitude/phi-deg']
                self.vehicle_state.pitch = self.fdm['attitude/theta-deg']
                self.vehicle_state.yaw = self.fdm['attitude/psi-deg']
                self.vehicle_state.lat = self.fdm['position/lat-geod-deg']
                self.vehicle_state.lon = self.fdm['position/long-gc-deg']
                self.vehicle_state.alt = self.fdm['position/h-sl-ft'] * 0.3048
            else:
                time.sleep(0.0001)
    
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