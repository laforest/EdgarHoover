#! /usr/bin/python3

import time
import sys

class SRF08:

    """
    Basic interface to the Devantech SRF-08 ultrasonic ranging module.
    Assumes an interface providing i2c_read and i2c_write. 
    """

    def __init__ (self, interface, address):
        self.interface  = interface
        self.address    = address
        self.ranges     = None
        self.light      = None

    def set_gain (self, gain):
        if gain < 1 or gain > 31:
            print("Error: gain out of range")
            sys.exit
        self.interface.i2c_write(self.address, 0x01, gain)

    def set_range (self, max_range):
        if max_range < 0 or max_range > 255:
            print("Error: max range out over limits")
            sys.exit
        self.interface.i2c_write(self.address, 0x02, max_range)

    def do_ranging (self):
        self.interface.i2c_write(self.address, 0x00, 0x51)
        time.sleep(0.070) # wait at least 70ms for ranging to finish
        
    def read_light (self):
        light = self.interface.i2c_read(self.address, 0x01, 1)
        self.light = int.from_bytes(light, "little")
        return light
    
    def read_ranges (self):
        ranges = []
        for register in range(2,36,2):
            range_byte_high = self.interface.i2c_read(self.address, register  , 1)
            range_byte_low  = self.interface.i2c_read(self.address, register+1, 1)
            this_range = range_byte_low + range_byte_high
            this_range = int.from_bytes(this_range, "little")
            ranges.append(this_range)
        self.ranges = ranges
        return ranges

    def set_i2c_address (self, new_address):
        self.interface.i2c_write(self.address, 0x00, 0xA0) 
        self.interface.i2c_write(self.address, 0x00, 0xAA) 
        self.interface.i2c_write(self.address, 0x00, 0xA5) 
        self.interface.i2c_write(self.address, 0x00, new_address) 

