from flight_dynamics import FlightDynamicsModel
from visuals import Visuals
from hardware_interface import HardwareInterface
import threading
from queue import Queue
from utils import *

if __name__ == "__main__":
    control_inputs_queue = Queue(1)
    simulated_sensors_queue = Queue(1)
    vehicle_state_queue = Queue(1)
    mouse_keyboard_controls_queue = Queue(1)

    fdm = FlightDynamicsModel(43.878960, -79.413383, mouse_keyboard_controls_queue, simulated_sensors_queue, vehicle_state_queue)
    visuals = Visuals(43.878960, -79.413383, vehicle_state_queue, mouse_keyboard_controls_queue)
    # hardware = HardwareInterface(control_inputs_queue, simulated_sensors_queue)

    visuals.run()