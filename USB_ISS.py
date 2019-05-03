#! /usr/bin/python3

"""
Implements the I2C adn UART functionality of the Devantech USB-ISS module
See: http://robot-electronics.co.uk/htm/usb_iss_tech.htm
Parameters are ints, but internally all data area bytes since the
file is opened in binary mode.
"""

import sys

class USB_ISS:

    def open (self):
        """
        No buffering to have a completely dumb terminal device
        Reads/writes work in bytes().
        """
        self.fd = open(self.device, mode = "r+b", buffering = 0)

    def get_config (self):
        command = bytes([0x5A, 0x01])
        self.fd.write(command)
        self.module_id, self.firmware_version, self.mode = self.fd.read(3)

    def __init__ (self, device = "/dev/ttyACM0"):
        self.device             = device
        self.fd                 = None
        self.module_id          = None
        self.firmware_version   = None
        self.mode               = None
        # UART buffer on USB_ISS
        self.uart_txbuffer_depth = 30
        # system UART receive buffer
        self.uart_rxbuffer      = bytearray()
        # Nothing works when device is not open (like UART receive)
        # so always open immediately
        self.open()
        self.set_i2c_serial_mode()

    def close (self):
        """All settings lost on close."""
        self.fd.close()

    def set_mode (self, mode, *parameters):
        parameters = list(parameters)
        command = bytes([0x5A, 0x02, mode] + parameters)
        self.fd.write(command)
        status          = self.fd.read(2)
        retval, errno   = status
        if retval != 0xFF:
            print("Mode set error: {0}".format(errno))
            sys.exit()
        self.get_config()

    def set_i2c_serial_mode (self):
        """Hardware I2C 400KHz and 57.6k serial"""
        self.set_mode(0x71, 0x00, 0x33)

    def i2c_test (self, address):
        command = bytes([0x58, address])
        self.fd.write(command)
        is_present = self.fd.read(1)
        # byte to int
        is_present = is_present[0]
        return is_present

    def i2c_test_all (self):
        present_devices = []
        for address in range(0, 256):
            is_present = self.i2c_test(address)
            if is_present != 0:
                present_devices.append(address)
        return present_devices

    def i2c_read (self, address, register, count):
        address = address + 1 # I2C read offset
        command = bytes([0x55, address, register, count])
        self.fd.write(command)
        read_val = self.fd.read(count)
        return read_val

    def i2c_write (self, address, register, *data):
        # Data should be <= 60 bytes (internal buffer)
        data    = list(data)
        count   = len(data)
        command = bytes([0x55, address, register, count] + data)
        self.fd.write(command)
        retval = self.fd.read(1)
        # byte to int
        retval = retval[0]
        return retval

    def uart_command (self, write_data = []):
        """Starts a SERIAL_IO command. len(write_data) must be <= 30."""
        # send empty list so we can write no data when reading
        command = bytes([0x62] + write_data)
        self.fd.write(command)

    def uart_status (self):
        """Ends the 0x62 (SERIAL_IO) command."""
        status_bytes  = self.fd.read(3)
        # byte to int
        status  = status_bytes[0]
        txcount = status_bytes[1]
        rxcount = status_bytes[2]
        # After a uart_status(), buffer any read data.
        data = self.fd.read(rxcount)
        self.uart_rxbuffer += data
        return status, txcount 

    def uart_read (self, count):
        # Fill buffer until enough data to perform read
        while len(self.uart_rxbuffer) < count:
            self.uart_command()
            self.uart_status()
        read_data           = self.uart_rxbuffer[0:count]
        self.uart_rxbuffer  = self.uart_rxbuffer[count:]
        return read_data

    def uart_write (self, write_data):
        while len(write_data) > 0:
            # How much free space in the write buffer?
            self.uart_command()
            status, txcount = self.uart_status()
            txfree          = self.uart_txbuffer_depth - txcount
            # Write as many as the buffer will hold
            write_count = min(len(write_data), txfree)
            self.uart_command(write_data[0:write_count])
            self.uart_status()
            write_data = write_data[write_count:]

