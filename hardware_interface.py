import serial
import struct

class HardwareInterface:
    def __init__(self):
        self.mouse_enable = False

        try:
            self.ser = serial.Serial("COM25", 115200)
        except serial.serialutil.SerialException: 
            print("Can't open port. Using mouse control.")
            self.mouse_enable = True

        self.input = (0, 0, 0)
    
    def read_inputs(self):
        return self.input
    
    def update(self):
        if not self.mouse_enable:
            rx_buff = self.ser.read(struct_size)
            struct_format = 'fff'
            struct_size = struct.calcsize(struct_format)
            self.input = struct.unpack(struct_format, rx_buff)