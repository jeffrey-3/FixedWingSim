from flight_dynamics import FlightDynamicsModel
from visuals import Visuals
from hardware_interface import HardwareInterface
import threading
from utils import *

class Simulator:
    def __init__(self):
        self.fdm = FlightDynamicsModel(43.878960, -79.413383)
        self.visuals = Visuals(43.8850443, -79.4124171, 2.2)
        self.hardware = HardwareInterface()

    def update_sim(self):
        while True:
            if self.hardware.mouse_enable:
                self.fdm.set_controls(
                    self.visuals.elevator, self.visuals.rudder, self.visuals.throttle
                )
            else:
                elevator, rudder, throttle = self.hardware.read_inputs()
                self.fdm.set_controls(elevator, rudder, throttle)

            if self.fdm.update():
                self.visuals.update_state(
                    self.fdm.get_fdm()['attitude/phi-deg'], 
                    self.fdm.get_fdm()['attitude/theta-deg'], 
                    self.fdm.get_fdm()['attitude/psi-deg'], 
                    self.fdm.get_fdm()['position/lat-geod-deg'],
                    self.fdm.get_fdm()['position/long-gc-deg'],
                    self.fdm.get_fdm()['position/h-sl-ft'] * 0.3048
                )
                self.hardware.send(self.fdm.get_fdm(), self.visuals.terrain_height)

    def start(self):
        threading.Thread(target=self.update_sim, daemon=True).start()
        self.visuals.run()

if __name__ == "__main__":
    sim = Simulator()
    sim.start()