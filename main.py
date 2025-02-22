import jsbsim

fdm = jsbsim.FGFDMExec(None)  # Use JSBSim default aircraft data.
fdm.load_script('scripts/c1723.xml')
fdm.run_ic()

print(fdm.get_delta_t())

while True:
    fdm.run()
    print(fdm.get_sim_time())