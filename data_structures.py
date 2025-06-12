from dataclasses import dataclass

@dataclass
class ControlInput:
    elevator: float = 0
    rudder: float = 0
    throttle: float = 0

@dataclass 
class SimulatedSensors:
    ax: float = 0
    ay: float = 0
    az: float = 0
    gx: float = 0
    gy: float = 0
    gz: float = 0
    mx: float = 0
    my: float = 0
    mz: float = 0
    baro_asl: float = 0
    gps_lat: float = 0
    gps_lon: float = 0
    of_x: float = 0
    of_y: float = 0

@dataclass
class VehicleState:
    roll: float = 0
    pitch: float = 0
    yaw: float = 0
    lat: float = 0
    lon: float = 0
    alt: float = 0