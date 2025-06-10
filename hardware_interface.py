import serial
import struct
import geomag
import numpy as np
import navpy
import math
import threading
import utils

class HardwareInterface:
    def __init__(self):
        self.mouse_enable = False

        self.input = (0, 0, 1001)

        try:
            self.ser = serial.Serial("COM25", 115200)
            threading.Thread(target=self.update, daemon=True).start()
        except serial.serialutil.SerialException: 
            print("Can't open port. Using mouse control.")
            self.mouse_enable = True
    
    def read_inputs(self):
        return self.input
    
    def send(self, fdm, terrain_height_m):
        if not self.mouse_enable:
            mag = self.est_mag(fdm['position/lat-geod-deg'], 
                               fdm['position/long-gc-deg'], 
                               fdm['attitude/phi-rad'], 
                               fdm['attitude/theta-rad'], 
                               fdm['attitude/psi-rad'] - math.pi)
            
            agl = fdm['position/h-sl-ft'] * 0.3048 - terrain_height_m

            tx_buff = struct.pack('=10f2i2h', 
                                  fdm['accelerations/n-pilot-x-norm'], 
                                  fdm['accelerations/n-pilot-y-norm'],
                                  fdm['accelerations/n-pilot-z-norm'],
                                  fdm['velocities/p-rad_sec'] * 180 / math.pi,
                                  fdm['velocities/q-rad_sec'] * 180 / math.pi,
                                  fdm['velocities/r-rad_sec'] * 180 / math.pi,
                                  -mag[0],
                                  -mag[1],
                                  -mag[2],
                                  fdm['position/h-sl-ft'] * 0.3048,
                                  int(fdm['position/lat-geod-deg'] * 1e7),
                                  int(fdm['position/long-gc-deg'] * 1e7),
                                  int(0),
                                  int(0))
            
            self.ser.write(tx_buff)
    
    def update(self):
        while True:
            struct_format = '3H'
            struct_size = struct.calcsize(struct_format)
            rx_buff = self.ser.read(struct_size)
            self.input = struct.unpack(struct_format, rx_buff)
            print(self.input)
    
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