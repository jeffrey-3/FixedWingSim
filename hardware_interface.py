import serial
from utils import *
import threading
from aplink.aplink_messages import *
from dataclasses import dataclass
from queue import Queue
import time
from flight_dynamics import SimulatedSensors

@dataclass
class ControlInput:
    elevator: float 
    rudder: float
    throttle: float

class HardwareInterface:
    def __init__(self, control_inputs_queue: Queue, simulated_sensors_queue: Queue):
        self.control_inputs_queue = control_inputs_queue
        self.simulated_sensors_queue = simulated_sensors_queue
        self.aplink = APLink()

    def connect(self, port: str, baud_rate: int) -> bool:
        try:
            self.serial_conn = serial.Serial(port, baud_rate)
            threading.Thread(target=self._receive_thread, daemon=True).start()
            threading.Thread(target=self._transmit_thread, daemon=True).start()
            return True
        except serial.serialutil.SerialException: 
            return False
    
    def _transmit_thread(self):
        while True:
            if self.simulated_sensors_queue.not_empty:
                simulated_sensors: SimulatedSensors = self.simulated_sensors_queue.get()
                self.serial_conn.write(
                    aplink_hitl_sensors().pack(
                        simulated_sensors.ax,
                        simulated_sensors.ay,
                        simulated_sensors.az,
                        simulated_sensors.gx,
                        simulated_sensors.gy,
                        simulated_sensors.gz,
                        simulated_sensors.mx,
                        simulated_sensors.my,
                        simulated_sensors.mz,
                        simulated_sensors.baro_asl,
                        simulated_sensors.gps_lat,
                        simulated_sensors.gps_lon,
                        simulated_sensors.of_x,
                        simulated_sensors.of_y
                    )
                )
            else:
                time.sleep(0.0001)
    
    def _receive_thread(self):
        while True:
            byte = self.serial_conn.read(1)
            result = self.aplink.parse_byte(ord(byte))
            if result is not None:
                payload, msg_id = result
                if msg_id == aplink_hitl_commands.msg_id:
                    msg = aplink_hitl_commands()
                    msg.unpack(payload)
                    self.control_inputs_queue.put(
                        ControlInput(
                            map_range(float(msg.ele_pwm), 1000, 2000, -1, 1),
                            map_range(float(msg.rud_pwm), 1000, 2000, -1, 1),
                            map_range(float(msg.thr_pwm), 1000, 2000, 0, 1)
                        )
                    )