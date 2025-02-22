import jsbsim
import time

fdm = jsbsim.FGFDMExec(None)  # Use JSBSim default aircraft data.
fdm.load_script('scripts/c1723.xml')
fdm.run_ic()

print(jsbsim.get_default_root_dir())

fdm.set_dt(0.01) # Run sim in background at 200hz

time.sleep(1)

start_time = time.time()
while True:
    sim_time = fdm.get_sim_time()
    real_time = time.time() - start_time

    if real_time >= sim_time:
        fdm.run()

        print(sim_time, fdm.get_property_value('attitude/psi-deg'), fdm.get_property_value('position/h-sl-ft'))