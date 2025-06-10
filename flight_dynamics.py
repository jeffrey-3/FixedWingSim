import jsbsim
import time
import utils

class FlightDynamicsModel:
    def __init__(self, initial_lat, initial_lon):
        self.initial_lat = initial_lat
        self.initial_lon = initial_lon
        self.fdm = jsbsim.FGFDMExec("models_jsbsim", None)
        self.fdm.load_model("YardStik")
        self.set_initial_conditions()
        self.fdm.run_ic()
        self.fdm.set_dt(0.008)
        self.start_time = time.time()
    
    def set_initial_conditions(self):
        self.fdm["ic/lat-geod-deg"] = self.initial_lat
        self.fdm["ic/long-gc-deg"] = self.initial_lon
        self.fdm["ic/h-sl-ft"] = 5
        self.fdm['attitude/phi-deg'] = 0
        self.fdm['attitude/theta-deg'] = 0
        self.fdm['ic/psi-true-deg'] = 0
        self.fdm["ic/vc-kts"] = 0

    def set_controls(self, elevator, rudder, throttle):
        self.fdm['fcs/elevator-cmd-norm'] = utils.map_range(elevator, 1000, 2000, -1, 1)
        self.fdm['fcs/aileron-cmd-norm'] = utils.map_range(rudder, 1000, 2000, -1, 1)
        self.fdm['fcs/throttle-cmd-norm'] = utils.map_range(throttle, 1000, 2000, 0, 1)

    def update(self):
        sim_time = self.fdm.get_sim_time()
        real_time = time.time() - self.start_time
        if real_time >= sim_time:
            self.fdm.run()
            return True
        return False
    
    def get_fdm(self):
        return self.fdm