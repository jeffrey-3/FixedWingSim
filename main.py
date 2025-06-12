from flight_dynamics import FlightDynamicsModel
from visuals import Visuals
from hardware_interface import HardwareInterface
from data_structures import *
import json

if __name__ == "__main__":
    config_file = open("config.json")
    params = json.load(config_file)

    control_inputs = ControlInput()
    simulated_sensors = SimulatedSensors()
    vehicle_state = VehicleState()
    mouse_keyboard_controls = ControlInput()

    hardware = HardwareInterface(control_inputs, simulated_sensors)
    
    if hardware.connect(params["serial_port"], params["baud_rate"]):
        print("Serial connected" + params["serial_port"])
        fdm_controls = control_inputs
    else:
        print("Serial failed to connect to " + params["serial_port"] + ", using mouse and keyboard controls instead")
        fdm_controls = mouse_keyboard_controls

    fdm = FlightDynamicsModel(
        params["initial_conditions"]["lat"], 
        params["initial_conditions"]["lon"], 
        fdm_controls, 
        simulated_sensors, 
        vehicle_state
    )

    visuals = Visuals(
        params["initial_conditions"]["lat"], 
        params["initial_conditions"]["lon"], 
        vehicle_state, 
        mouse_keyboard_controls
    )

    visuals.run()