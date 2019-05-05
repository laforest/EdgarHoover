#! /usr/bin/python3

import serial
import sys

class Communication_Interfaces:

    """Abstracts I2C and UART interfaces for other classes"""

    def __init__ (self, uart_device = "/dev/ttyUSB0", uart_baudrate = 57600):
        self.uart_device    = uart_device
        self.uart_baudrate  = uart_baudrate
        # No timeout!
        self.uart_fd        = serial.Serial(self.uart_device, self.uart_baudrate)

    def uart_read (self, count):
        # Can't error out: blocks until count bytes read when no timeout set
        return self.uart_fd.read(count)

    def uart_write (self, data):
        bytes_to_write  = len(data)
        bytes_written   = self.uart_fd.write(data)
        if bytes_written != bytes_to_write:
            print("UART write error! Had {0} bytes, but only wrote {1}.".format(bytes_to_write, bytes_written))
            sys.exit()

if __name__ == "__main__":
    CI = Communication_Interfaces()
    print("Testing UART loopback")
    test_string = b"Test data passed through loopback!"
    test_len = len(test_string)
    CI.uart_write(test_string)
    print(CI.uart_read(test_len))
    print("Done!")

