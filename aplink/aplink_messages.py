
# Auto-generated Python

import struct
from enum import IntEnum
from aplink.aplink_helpers import APLink
                    

class PARAM_TYPE(IntEnum):
    
    INT32 = 0,
    
    FLOAT = 1,
    

class COMMAND_ID(IntEnum):
    
    CALIBRATE = 0,
    

class MODE_ID(IntEnum):
    
    CONFIG = 0,
    
    STARTUP = 1,
    
    MANUAL = 2,
    
    FBW = 3,
    
    TAKEOFF = 4,
    
    MISSION = 5,
    
    LAND = 6,
    
    FLARE = 7,
    
    UNKNOWN = 8,
    

class MISSION_ITEM_TYPE(IntEnum):
    
    WAYPOINT = 0,
    
    LOITER = 1,
    
    LAND = 2,
    

class LOITER_DIRECTION(IntEnum):
    
    LEFT = 0,
    
    RIGHT = 1,
    
 

        
class aplink_vehicle_status_full:
    msg_id = 0  
                      
    
    roll = None             
    
    pitch = None             
    
    yaw = None             
    
    alt = None             
    
    spd = None             
    
    lat = None             
    
    lon = None             
    
    mode_id = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=hhhhhiiB", payload)
        offset = 0
                    
        
        
        self.roll = unpack[offset]
        offset += 1
        
        
        
        self.pitch = unpack[offset]
        offset += 1
        
        
        
        self.yaw = unpack[offset]
        offset += 1
        
        
        
        self.alt = unpack[offset]
        offset += 1
        
        
        
        self.spd = unpack[offset]
        offset += 1
        
        
        
        self.lat = unpack[offset]
        offset += 1
        
        
        
        self.lon = unpack[offset]
        offset += 1
        
        
        
        self.mode_id = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, roll, pitch, yaw, alt, spd, lat, lon, mode_id):
        payload = struct.pack("=hhhhhiiB", roll, pitch, yaw, alt, spd, lat, lon, mode_id)
        return APLink().pack(payload, self.msg_id)
        
class aplink_control_setpoints:
    msg_id = 1  
                      
    
    roll_sp = None             
    
    pitch_sp = None             
    
    alt_sp = None             
    
    spd_sp = None             
    
    current_waypoint = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=hhhhB", payload)
        offset = 0
                    
        
        
        self.roll_sp = unpack[offset]
        offset += 1
        
        
        
        self.pitch_sp = unpack[offset]
        offset += 1
        
        
        
        self.alt_sp = unpack[offset]
        offset += 1
        
        
        
        self.spd_sp = unpack[offset]
        offset += 1
        
        
        
        self.current_waypoint = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, roll_sp, pitch_sp, alt_sp, spd_sp, current_waypoint):
        payload = struct.pack("=hhhhB", roll_sp, pitch_sp, alt_sp, spd_sp, current_waypoint)
        return APLink().pack(payload, self.msg_id)
        
class aplink_gps_raw:
    msg_id = 2  
                      
    
    lat = None             
    
    lon = None             
    
    sats = None             
    
    fix = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=iiB?", payload)
        offset = 0
                    
        
        
        self.lat = unpack[offset]
        offset += 1
        
        
        
        self.lon = unpack[offset]
        offset += 1
        
        
        
        self.sats = unpack[offset]
        offset += 1
        
        
        
        self.fix = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, lat, lon, sats, fix):
        payload = struct.pack("=iiB?", lat, lon, sats, fix)
        return APLink().pack(payload, self.msg_id)
        
class aplink_power:
    msg_id = 3  
                      
    
    batt_volt = None             
    
    batt_curr = None             
    
    batt_used = None             
    
    ap_curr = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=HHHH", payload)
        offset = 0
                    
        
        
        self.batt_volt = unpack[offset]
        offset += 1
        
        
        
        self.batt_curr = unpack[offset]
        offset += 1
        
        
        
        self.batt_used = unpack[offset]
        offset += 1
        
        
        
        self.ap_curr = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, batt_volt, batt_curr, batt_used, ap_curr):
        payload = struct.pack("=HHHH", batt_volt, batt_curr, batt_used, ap_curr)
        return APLink().pack(payload, self.msg_id)
        
class aplink_rc_input:
    msg_id = 4  
                      
    
    ail = None             
    
    ele = None             
    
    rud = None             
    
    thr = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=bbbb", payload)
        offset = 0
                    
        
        
        self.ail = unpack[offset]
        offset += 1
        
        
        
        self.ele = unpack[offset]
        offset += 1
        
        
        
        self.rud = unpack[offset]
        offset += 1
        
        
        
        self.thr = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, ail, ele, rud, thr):
        payload = struct.pack("=bbbb", ail, ele, rud, thr)
        return APLink().pack(payload, self.msg_id)
        
class aplink_cal_sensors:
    msg_id = 5  
                      
    
    gx = None             
    
    gy = None             
    
    gz = None             
    
    ax = None             
    
    ay = None             
    
    az = None             
    
    mx = None             
    
    my = None             
    
    mz = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=fffffffff", payload)
        offset = 0
                    
        
        
        self.gx = unpack[offset]
        offset += 1
        
        
        
        self.gy = unpack[offset]
        offset += 1
        
        
        
        self.gz = unpack[offset]
        offset += 1
        
        
        
        self.ax = unpack[offset]
        offset += 1
        
        
        
        self.ay = unpack[offset]
        offset += 1
        
        
        
        self.az = unpack[offset]
        offset += 1
        
        
        
        self.mx = unpack[offset]
        offset += 1
        
        
        
        self.my = unpack[offset]
        offset += 1
        
        
        
        self.mz = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, gx, gy, gz, ax, ay, az, mx, my, mz):
        payload = struct.pack("=fffffffff", gx, gy, gz, ax, ay, az, mx, my, mz)
        return APLink().pack(payload, self.msg_id)
        
class aplink_mission_item:
    msg_id = 6  
                      
    
    type = None             
    
    lat = None             
    
    lon = None             
    
    radius = None             
    
    direction = None             
    
    final_leg = None             
    
    glideslope = None             
    
    runway_heading = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=BiifBfff", payload)
        offset = 0
                    
        
        
        self.type = unpack[offset]
        offset += 1
        
        
        
        self.lat = unpack[offset]
        offset += 1
        
        
        
        self.lon = unpack[offset]
        offset += 1
        
        
        
        self.radius = unpack[offset]
        offset += 1
        
        
        
        self.direction = unpack[offset]
        offset += 1
        
        
        
        self.final_leg = unpack[offset]
        offset += 1
        
        
        
        self.glideslope = unpack[offset]
        offset += 1
        
        
        
        self.runway_heading = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, type, lat, lon, radius, direction, final_leg, glideslope, runway_heading):
        payload = struct.pack("=BiifBfff", type, lat, lon, radius, direction, final_leg, glideslope, runway_heading)
        return APLink().pack(payload, self.msg_id)
        
class aplink_hitl_sensors:
    msg_id = 7  
                      
    
    imu_ax = None             
    
    imu_ay = None             
    
    imu_az = None             
    
    imu_gx = None             
    
    imu_gy = None             
    
    imu_gz = None             
    
    mag_x = None             
    
    mag_y = None             
    
    mag_z = None             
    
    baro_asl = None             
    
    gps_lat = None             
    
    gps_lon = None             
    
    of_x = None             
    
    of_y = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=ffffffffffiihh", payload)
        offset = 0
                    
        
        
        self.imu_ax = unpack[offset]
        offset += 1
        
        
        
        self.imu_ay = unpack[offset]
        offset += 1
        
        
        
        self.imu_az = unpack[offset]
        offset += 1
        
        
        
        self.imu_gx = unpack[offset]
        offset += 1
        
        
        
        self.imu_gy = unpack[offset]
        offset += 1
        
        
        
        self.imu_gz = unpack[offset]
        offset += 1
        
        
        
        self.mag_x = unpack[offset]
        offset += 1
        
        
        
        self.mag_y = unpack[offset]
        offset += 1
        
        
        
        self.mag_z = unpack[offset]
        offset += 1
        
        
        
        self.baro_asl = unpack[offset]
        offset += 1
        
        
        
        self.gps_lat = unpack[offset]
        offset += 1
        
        
        
        self.gps_lon = unpack[offset]
        offset += 1
        
        
        
        self.of_x = unpack[offset]
        offset += 1
        
        
        
        self.of_y = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, imu_ax, imu_ay, imu_az, imu_gx, imu_gy, imu_gz, mag_x, mag_y, mag_z, baro_asl, gps_lat, gps_lon, of_x, of_y):
        payload = struct.pack("=ffffffffffiihh", imu_ax, imu_ay, imu_az, imu_gx, imu_gy, imu_gz, mag_x, mag_y, mag_z, baro_asl, gps_lat, gps_lon, of_x, of_y)
        return APLink().pack(payload, self.msg_id)
        
class aplink_hitl_commands:
    msg_id = 8  
                      
    
    rud_pwm = None             
    
    ele_pwm = None             
    
    thr_pwm = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=HHH", payload)
        offset = 0
                    
        
        
        self.rud_pwm = unpack[offset]
        offset += 1
        
        
        
        self.ele_pwm = unpack[offset]
        offset += 1
        
        
        
        self.thr_pwm = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, rud_pwm, ele_pwm, thr_pwm):
        payload = struct.pack("=HHH", rud_pwm, ele_pwm, thr_pwm)
        return APLink().pack(payload, self.msg_id)
        
class aplink_set_altitude:
    msg_id = 9  
                      
    
    altitude = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=f", payload)
        offset = 0
                    
        
        
        self.altitude = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, altitude):
        payload = struct.pack("=f", altitude)
        return APLink().pack(payload, self.msg_id)
        
class aplink_set_altitude_result:
    msg_id = 10  
                      
    
    success = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=?", payload)
        offset = 0
                    
        
        
        self.success = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, success):
        payload = struct.pack("=?", success)
        return APLink().pack(payload, self.msg_id)
        
class aplink_waypoints_count:
    msg_id = 11  
                      
    
    num_waypoints = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=B", payload)
        offset = 0
                    
        
        
        self.num_waypoints = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, num_waypoints):
        payload = struct.pack("=B", num_waypoints)
        return APLink().pack(payload, self.msg_id)
        
class aplink_request_waypoint:
    msg_id = 12  
                      
    
    index = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=B", payload)
        offset = 0
                    
        
        
        self.index = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, index):
        payload = struct.pack("=B", index)
        return APLink().pack(payload, self.msg_id)
        
class aplink_waypoints_ack:
    msg_id = 13  
                      
    
    success = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=?", payload)
        offset = 0
                    
        
        
        self.success = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, success):
        payload = struct.pack("=?", success)
        return APLink().pack(payload, self.msg_id)
        
class aplink_time_since_epoch:
    msg_id = 14  
                      
    
    microseconds = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=Q", payload)
        offset = 0
                    
        
        
        self.microseconds = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, microseconds):
        payload = struct.pack("=Q", microseconds)
        return APLink().pack(payload, self.msg_id)
        
class aplink_param_set:
    msg_id = 15  
                      
    
    name = []             
    
    value = []             
    
    type = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=BBBBBBBBBBBBBBBBBBBBB", payload)
        offset = 0
                    
        
        
        self.name = unpack[offset:offset+16]
        offset += 16
        
        
        
        self.value = unpack[offset:offset+4]
        offset += 4
        
        
        
        self.type = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, name, value, type):
        payload = struct.pack("=BBBBBBBBBBBBBBBBBBBBB", *name, *value, type)
        return APLink().pack(payload, self.msg_id)
        
class aplink_command:
    msg_id = 16  
                      
    
    command_id = None             
    
    
    def unpack(self, payload: bytes):
        unpack = struct.unpack("=B", payload)
        offset = 0
                    
        
        
        self.command_id = unpack[offset]
        offset += 1
        
        
                    
        return True
    
    def pack(self, command_id):
        payload = struct.pack("=B", command_id)
        return APLink().pack(payload, self.msg_id)
