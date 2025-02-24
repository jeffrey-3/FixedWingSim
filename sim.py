import jsbsim
import time
from tabulate import tabulate

class Simulator:
    def __init__(self):
        self.fdm = jsbsim.FGFDMExec("models_jsbsim", None)  # Use JSBSim default aircraft data.
        self.fdm.set_dt(0.005) # Run sim in background at 200hz
        self.start_time = time.time()
        self.last_print_time = time.time()

        # Load aircraft model
        self.fdm.load_model("Rascal110")

        self.set_initial_conditions()
        self.fdm.run_ic()
    
    def set_initial_conditions(self):
        self.fdm["ic/lat-geod-deg"] = 38.897957
        self.fdm["ic/long-gc-deg"] = -77.036560
        self.fdm["ic/h-sl-ft"] = 100
        self.fdm['ic/psi-true-deg'] = 0
        self.fdm["ic/vc-kts"] = 30

    def run(self):
        sim_time = self.fdm.get_sim_time()
        real_time = time.time() - self.start_time

        if real_time >= sim_time:
            ptch_sp = 0.1 * (200 - self.fdm['position/h-sl-ft'])
            self.fdm['fcs/aileron-cmd-norm'] = 0.02 * (20 - self.fdm['attitude/phi-deg']) # P controller wing leveller
            self.fdm['fcs/elevator-cmd-norm'] = -1 * 0.02 * (ptch_sp - self.fdm['attitude/theta-deg'])
            self.fdm['fcs/throttle-cmd-norm'] = 0.7

            self.fdm.run()

            if time.time() - self.last_print_time > 0.3:
                headers = ["Time", "Roll", "Pitch", "Heading", "Alt", "Lat", "Lon", "Spd", "Thr"]
                data = [[
                    f"{sim_time:.1f}",
                    f"{self.fdm['attitude/phi-deg']:.1f}",
                    f"{self.fdm['attitude/theta-deg']:.1f}",
                    f"{self.fdm['attitude/psi-deg']:.1f}",
                    f"{self.fdm['position/h-sl-ft']:.1f}",
                    f"{self.fdm['position/lat-geod-deg']:.7f}",
                    f"{self.fdm['position/long-gc-deg']:.7f}",
                    f"{self.fdm['velocities/vc-kts']:.1f}",
                    f"{self.fdm['fcs/throttle-cmd-norm']:.2f}"
                ]]
                
                print(tabulate(data, headers=headers, tablefmt="plain"))
                print()
                
                self.last_print_time = time.time()
    
    def get_fdm(self):
        return self.fdm