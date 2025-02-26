import serial
import struct
import geomag
import numpy as np
import navpy

class HardwareInterface:
    def __init__(self):
        self.mouse_enable = False

        try:
            self.ser = serial.Serial("COM25", 115200)
        except serial.serialutil.SerialException: 
            print("Can't open port. Using mouse control.")
            self.mouse_enable = True

        self.input = (0, 0, 0)
    
    def read_inputs(self):
        return self.input
    
    def send(self, fdm):
        if not self.mouse_enable:
            mag = self.est_mag(fdm['position/lat-geod-deg'], 
                            fdm['position/long-gc-deg'], 
                            fdm['attitude/phi-rad'], 
                            fdm['attitude/theta-rad'], 
                            fdm['attitude/psi-rad'])
                
            tx_buff = struct.pack('<13f', fdm['accelerations/Nx'], 
                                        fdm['accelerations/Ny'],
                                        fdm['accelerations/Nz'],
                                        fdm['velocities/p-rad_sec'],
                                        fdm['velocities/q-rad_sec'],
                                        fdm['velocities/r-rad_sec'],
                                        mag[0],
                                        mag[1],
                                        mag[2],
                                        fdm['position/h-sl-ft'],
                                        fdm['position/lat-geod-deg'],
                                        fdm['position/long-gc-deg'],
                                        fdm['position/h-agl-ft'])
            
            self.ser.write(tx_buff)
    
    def update(self):
        if not self.mouse_enable:
            rx_buff = self.ser.read(struct_size)
            struct_format = 'fff'
            struct_size = struct.calcsize(struct_format)
            self.input = struct.unpack(struct_format, rx_buff)
    
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