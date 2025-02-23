import jsbsim
import time

# Ref: https://github.com/AOS55/Fixedwing-Airsim/blob/master/src/jsbsim_properties.py

class Simulator:
    def __init__(self):
        self.fdm = jsbsim.FGFDMExec("models_jsbsim", None)  # Use JSBSim default aircraft data.
        self.fdm.set_dt(0.005) # Run sim in background at 200hz
        self.start_time = time.time()

        # Load aircraft model
        self.fdm.load_model("Rascal110")

        self.set_initial_conditions()
    
    def set_initial_conditions(self):
        self.fdm["ic/lat-geod-deg"] = 38.897957
        self.fdm["ic/long-gc-deg"] = -77.036560
        self.fdm["ic/h-sl-ft"] = 10
        self.fdm['ic/psi-true-deg'] = 0
        self.fdm["ic/vc-kts"] = 0
        self.fdm["propulsion/set-running"] = -1

    def run(self):
        sim_time = self.fdm.get_sim_time()
        real_time = time.time() - self.start_time

        if real_time >= sim_time:
            self.fdm.run()

            print(
                f"{sim_time:.3f}\t"
                f"{self.fdm.get_property_value('attitude/psi-deg'):.1f}\t"
                f"{self.fdm.get_property_value('position/h-sl-ft'):.2f}\t"
                f"{self.fdm.get_property_value('position/lat-geod-deg'):.7f}\t"
                f"{self.fdm.get_property_value('position/long-gc-deg'):.7f}\t"
            )