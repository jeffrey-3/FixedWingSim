import struct
import crcmod
from typing import Optional, Tuple

class APLink:
    """Python implementation of the APLink protocol"""
    
    START_BYTE = 0xFE
    HEADER_LEN = 3
    FOOTER_LEN = 2
    MAX_PAYLOAD_LEN = 255
    MAX_PACKET_LEN = MAX_PAYLOAD_LEN + HEADER_LEN + FOOTER_LEN
    
    def __init__(self):
        self._crc16 = crcmod.mkCrcFun(0x18005, initCrc=0xFFFF, xorOut=0x0000, rev=False)
        self._reset_parser()
    
    def _reset_parser(self):
        """Reset the parser state"""
        self._buffer = bytearray()
        self._expected_len = 0
        self._parsing = False
    
    def parse_byte(self, byte: int) -> Optional[Tuple[bytes, int]]:
        """
        Parse a single byte from the stream
        Returns: (payload, msg_id) if complete message found, None otherwise
        """
        if not self._parsing and byte == self.START_BYTE:
            self._parsing = True
            self._buffer = bytearray([byte])
            return None
        
        if self._parsing:
            self._buffer.append(byte)
            
            # After header, we know the expected length
            if len(self._buffer) == self.HEADER_LEN:
                payload_len = self._buffer[1]
                self._expected_len = self.HEADER_LEN + payload_len + self.FOOTER_LEN
            
            # Check if we have a complete packet
            if len(self._buffer) == self._expected_len:
                result = self.unpack(bytes(self._buffer))
                self._reset_parser()
                return result
        
        return None
    
    def unpack(self, packet: bytes) -> Optional[Tuple[bytes, int]]:
        """Unpack a complete APLink packet"""
        if len(packet) < self.HEADER_LEN + self.FOOTER_LEN:
            print("aplink len too small")
            return None
            
        if packet[0] != self.START_BYTE:
            print("aplink start byte wrong")
            return None
            
        payload_len = packet[1]
        msg_id = packet[2]
        
        if len(packet) != self.HEADER_LEN + payload_len + self.FOOTER_LEN:
            print("aplink len small 2")
            return None
        
        # Verify checksum (excludes START_BYTE)
        body = packet[1:-2]
        expected_crc = self._crc16(body)
        received_crc = (packet[-2] << 8) | packet[-1]
        
        if expected_crc != received_crc:
            print("aplink checksum wrong")
            print(expected_crc, received_crc)
            return None
            
        payload = packet[self.HEADER_LEN:self.HEADER_LEN+payload_len]

        return (payload, msg_id)
    
    def pack(self, payload: bytes, msg_id: int) -> bytes:
        """Pack a payload into an APLink packet"""
        if len(payload) > self.MAX_PAYLOAD_LEN:
            raise ValueError("Payload too large")
            
        header = struct.pack('=BBB', self.START_BYTE, len(payload), msg_id)
        body = header[1:] + payload  # For checksum calculation
        checksum = self._crc16(body)
        footer = struct.pack('>H', checksum)
        
        return header + payload + footer

    def calculate_packet_size(self, payload_len):
        return self.HEADER_LEN + payload_len + self.FOOTER_LEN