import jsbsim
import time
from utils import *

def calculate_pitch_roll(accel):
    ax, ay, az = accel  # Accelerometer readings (m/s²)
    
    pitch = math.atan2(-ax, math.sqrt(ay**2 + az**2)) * (180.0 / math.pi)
    roll = math.atan2(ay, az) * (180.0 / math.pi)
    
    return pitch, roll

class FlightDynamicsModel:
    def __init__(self):
        self.fdm = jsbsim.FGFDMExec("models_jsbsim", None)  # Use JSBSim default aircraft data.
        self.fdm.set_dt(0.008) # Run sim in background at 125Hz
        self.start_time = time.time()

        # Load aircraft model
        self.fdm.load_model("Rascal110")

        self.set_initial_conditions()
        self.fdm.run_ic()

        self.initial_lat = self.fdm['position/lat-geod-deg']
        self.initial_lon = self.fdm['position/long-gc-deg']

        print(self.fdm.get_property_catalog())
    
    def set_initial_conditions(self):
        self.fdm["ic/lat-geod-deg"] = 43.878960
        self.fdm["ic/long-gc-deg"] = -79.413383
        self.fdm["ic/h-sl-ft"] = 5
        self.fdm['attitude/phi-deg'] = 0
        self.fdm['attitude/theta-deg'] = 0
        self.fdm['ic/psi-true-deg'] = 0
        self.fdm["ic/vc-kts"] = 0

    def set_controls(self, aileron, elevator, throttle):
        self.fdm['fcs/aileron-cmd-norm'] = aileron
        self.fdm['fcs/elevator-cmd-norm'] = elevator
        self.fdm['fcs/throttle-cmd-norm'] = throttle

    def update(self):
        sim_time = self.fdm.get_sim_time()
        real_time = time.time() - self.start_time

        if real_time >= sim_time:
            self.fdm.run()

            pitch, roll = calculate_pitch_roll((-self.fdm['accelerations/n-pilot-x-norm'], 
                                                -self.fdm['accelerations/n-pilot-y-norm'], 
                                                -self.fdm['accelerations/n-pilot-z-norm']))
            print(f"{sim_time:.3f} " +
                  f"{self.fdm['accelerations/n-pilot-x-norm']:.2f} " + 
                  f"{self.fdm['accelerations/n-pilot-y-norm']:.2f} " + 
                  f"{self.fdm['accelerations/n-pilot-z-norm']:.2f} " +
                  f"{pitch:.2f} " +
                  f"{roll:.2f}")
            
            return True
        return False
    
    def get_fdm(self):
        return self.fdm