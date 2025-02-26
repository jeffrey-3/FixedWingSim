import jsbsim
import time
import struct
from tabulate import tabulate
import geomag
import navpy
import serial
import numpy as np
from utils import *

class FlightDynamicsModel:
    def __init__(self):
        self.fdm = jsbsim.FGFDMExec("models_jsbsim", None)  # Use JSBSim default aircraft data.
        self.fdm.set_dt(0.005) # Run sim in background at 200hz
        self.start_time = time.time()
        self.last_print_time = time.time()

        # Load aircraft model
        self.fdm.load_model("Rascal110")

        self.set_initial_conditions()
        self.fdm.run_ic()

        self.initial_lat = self.fdm['position/lat-geod-deg']
        self.initial_lon = self.fdm['position/long-gc-deg']
    
    def set_initial_conditions(self):
        self.fdm["ic/lat-geod-deg"] = 38.897957
        self.fdm["ic/long-gc-deg"] = -77.036560
        self.fdm["ic/h-sl-ft"] = 5
        self.fdm['attitude/phi-deg'] = 0
        self.fdm['attitude/theta-deg'] = 0
        self.fdm['ic/psi-true-deg'] = 0
        self.fdm["ic/vc-kts"] = 0
        self.fdm['fcs/throttle-cmd-norm'] = 0.0001
    
    def est_mag(self, lat_deg, lon_deg, phi_rad, the_rad, psi_rad):
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

    def set_controls(self, aileron, elevator, throttle):
        self.fdm['fcs/aileron-cmd-norm'] = aileron
        self.fdm['fcs/elevator-cmd-norm'] = elevator
        self.fdm['fcs/throttle-cmd-norm'] = throttle

    def update(self):
        sim_time = self.fdm.get_sim_time()
        real_time = time.time() - self.start_time

        if real_time >= sim_time:
            self.fdm.run()

            if time.time() - self.last_print_time > 0.2:
                self.print()
                self.last_print_time = time.time()

        # mag = self.est_mag(self.fdm['position/lat-geod-deg'], 
        #                        self.fdm['position/long-gc-deg'], 
        #                        self.fdm['attitude/phi-rad'], 
        #                        self.fdm['attitude/theta-rad'], 
        #                        self.fdm['attitude/psi-rad'])
            
        # tx_buff = struct.pack('<13f', self.fdm['accelerations/Nx'], 
        #                               self.fdm['accelerations/Ny'],
        #                               self.fdm['accelerations/Nz'],
        #                               self.fdm['velocities/p-rad_sec'],
        #                               self.fdm['velocities/q-rad_sec'],
        #                               self.fdm['velocities/r-rad_sec'],
        #                               mag[0],
        #                               mag[1],
        #                               mag[2],
        #                               self.fdm['position/h-sl-ft'],
        #                               self.fdm['position/lat-geod-deg'],
        #                               self.fdm['position/long-gc-deg'],
        #                               self.fdm['position/h-agl-ft'])
        
        # north, east = calculate_north_east(self.fdm['position/lat-geod-deg'],
        #                                    self.fdm['position/long-gc-deg'],
        #                                    self.center_lat,
        #                                    self.center_lon)
        
        # return self.fdm['attitude/phi-deg'], self.fdm['attitude/theta-deg'], self.fdm['attitude/psi-deg'], north, east, -self.fdm['position/h-sl-ft'] * 0.3048
    
    def get_fdm(self):
        return self.fdm

    def print(self):
        headers = ["Time", "Roll", "Pitch", "Heading", "Alt", "Lat", "Lon", "Spd", "Thr", "acc_x", "acc_y", "acc_z"]
        data = [[
            f"{self.fdm.get_sim_time():.1f}",
            f"{self.fdm['attitude/phi-deg']:.1f}",
            f"{self.fdm['attitude/theta-deg']:.1f}",
            f"{self.fdm['attitude/psi-deg']:.1f}",
            f"{self.fdm['position/h-sl-ft'] * 0.3048:.1f}",
            f"{self.fdm['position/lat-geod-deg']:.7f}",
            f"{self.fdm['position/long-gc-deg']:.7f}",
            f"{self.fdm['velocities/vc-kts']:.1f}",
            f"{self.fdm['fcs/throttle-cmd-norm']:.2f}",
            f"{self.fdm['accelerations/Nx']:.2f}",
            f"{self.fdm['accelerations/Ny']:.2f}",
            f"{self.fdm['accelerations/Nz']:.2f}"
        ]]
        print(tabulate(data, headers=headers, tablefmt="plain"))
        print()