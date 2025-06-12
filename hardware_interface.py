import serial
from utils import *
import threading
from aplink.aplink_messages import *
from data_structures import *
from queue import Queue
import time

class HardwareInterface:
    def __init__(self, control_input: ControlInput, simulated_sensors: SimulatedSensors):
        self.control_input = control_input
        self.simulated_sensors = simulated_sensors
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
            self.serial_conn.write(
                aplink_hitl_sensors().pack(
                    self.simulated_sensors.ax,
                    self.simulated_sensors.ay,
                    self.simulated_sensors.az,
                    self.simulated_sensors.gx,
                    self.simulated_sensors.gy,
                    self.simulated_sensors.gz,
                    self.simulated_sensors.mx,
                    self.simulated_sensors.my,
                    self.simulated_sensors.mz,
                    self.simulated_sensors.baro_asl,
                    self.simulated_sensors.gps_lat,
                    self.simulated_sensors.gps_lon,
                    self.simulated_sensors.of_x,
                    self.simulated_sensors.of_y
                )
            )

            time.sleep(0.005)
    
    def _receive_thread(self):
        while True:
            byte = self.serial_conn.read(1)
            # print(byte)
            result = self.aplink.parse_byte(ord(byte))
            if result is not None:
                payload, msg_id = result
                if msg_id == aplink_hitl_commands.msg_id:
                    msg = aplink_hitl_commands()
                    msg.unpack(payload)

                    self.control_input.elevator = map_range(float(msg.ele_pwm), 1000, 2000, -1, 1)
                    self.control_input.rudder = map_range(float(msg.rud_pwm), 1000, 2000, -1, 1)
                    self.control_input.throttle = map_range(float(msg.thr_pwm), 1000, 2000, 0, 1)

                    print(vars(self.control_input))