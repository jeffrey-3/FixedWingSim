import jsbsim
import time
from utils import *

class FlightDynamicsModel:
    def __init__(self):
        self.fdm = jsbsim.FGFDMExec("models_jsbsim", None)
        self.fdm.load_model("YardStik")
        self.set_initial_conditions()
        self.fdm.run_ic()
        self.fdm.set_dt(0.008)
        self.start_time = time.time()
    
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
            return True
        return False
    
    def get_fdm(self):
        return self.fdm