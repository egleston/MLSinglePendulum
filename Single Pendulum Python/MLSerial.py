import serial
import serial.tools.list_ports
import threading

def find_port(prefix):
    """Retourne le premier port dont le nom commence par `prefix`, ou None."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if port.device.startswith(prefix):
            return port.device
    return None

# get the open serial port
def get_serial_port()->serial.Serial:
    serialPrefix = "/dev/cu.usbmodem"
    serialName = find_port(serialPrefix)

    if serialName is None:
        print(f"No port starting with '{serialPrefix}' found.")
        print("Available ports:")
        for p in serial.tools.list_ports.comports():
            print(f"  {p.device}")
        return  None
    else:
        try:
            ser = serial.Serial(
                serialName, 115200,
                parity=serial.PARITY_NONE,
                bytesize=serial.EIGHTBITS,
                stopbits=serial.STOPBITS_ONE
            )
            print(f"Connected to {serialName}")
            return ser
        except serial.SerialException as e:
            print(f"Error: unable to open {serialName} — {e}")
            return  None

import threading
import struct

SYNC_BYTE = 0xAA
PACKET_SIZE = 26  # 1 octet sync + 6 x 4 bytes (6 floats)

class SerialReader:
    def __init__(self, serial_port):
        self.serial = serial_port
        self.running = False
        self.thread = None
        self.callback = None  # function to call with received values

    def start(self, callback=None):
        self.callback = callback
        self.running = True
        self.thread = threading.Thread(target=self._read_loop, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)

    def _read_loop(self):
        while self.running:
            try:
                # 1. Synchronisation : search for SYNC_BYTE (0xAA)
                if self.serial is None:
                    return
                byte = self.serial.read(1)
                if not byte or byte[0] != SYNC_BYTE:
                    continue

                # 2. Read the next 24 bytes (6 floats)
                data = self.serial.read(24)
                if len(data) < 24:
                    continue  # incomplete packet, skip and wait for the next one

                # 3. Decode the 6 floats (little-endian)
                floats = struct.unpack('<6f', data)

                # 4. To call the callback with the received values
                if self.callback:
                    self.callback(floats)

            except Exception as e:
                print(f"Error : {e}")
                break