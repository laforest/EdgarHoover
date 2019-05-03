#! /usr/bin/python3

from USB_ISS import USB_ISS
import time
import sys

class SRF08:

    def __init__ (self, usb_iss, address):
        self.usb_iss    = usb_iss
        self.address    = address
        self.ranges     = None
        self.light      = None

    def set_gain (self, gain):
        if gain < 1 or gain > 31:
            print("Error: gain out of range")
            sys.exit
        self.usb_iss.i2c_write(self.address, 0x01, 1, gain)

    def set_range (self, max_range):
        if max_range < 0 or max_range > 255:
            print("Error: max range out over limits")
            sys.exit
        self.usb_iss.i2c_write(self.address, 0x02, 1, max_range)

    def do_ranging (self):
        self.usb_iss.i2c_write(self.address, 0x00, 1, 0x51)
        time.sleep(0.070) # wait at least 70ms for ranging to finish
        
    def read_light (self):
        light = self.usb_iss.i2c_read(self.address, 0x01, 1)
        self.light = int.from_bytes(light, "little")
        return light
    
    def read_ranges (self):
        ranges = []
        for register in range(2,36,2):
            range_byte_high = self.usb_iss.i2c_read(self.address, register  , 1)
            range_byte_low  = self.usb_iss.i2c_read(self.address, register+1, 1)
            this_range = range_byte_low + range_byte_high
            this_range = int.from_bytes(this_range, "little")
            ranges.append(this_range)
        self.ranges = ranges
        return ranges

    def set_i2c_address (self, new_address):
        self.usb_iss.i2c_write(self.address, 0x00, 1, 0xA0) 
        self.usb_iss.i2c_write(self.address, 0x00, 1, 0xAA) 
        self.usb_iss.i2c_write(self.address, 0x00, 1, 0xA5) 
        self.usb_iss.i2c_write(self.address, 0x00, 1, new_address) 

def test ():
    iss = USB_ISS()
    #iss.open()
    #iss.set_i2c_serial_mode()
    #iss.get_config()
    #iss.i2c_test_all()

#    srf1 = SRF08(iss, 0xFC)
#    srf1.set_gain(31)
#    srf1.set_range(255)
#    srf1.do_ranging()
#    srf1.read_light()
#    srf1.read_ranges()
#    print(srf1.light)
#    print(srf1.ranges)
#
#    srf2 = SRF08(iss, 0xFE)
#    srf2.set_gain(31)
#    srf2.set_range(255)
#    srf2.do_ranging()
#    srf2.read_light()
#    srf2.read_ranges()
#    print(srf2.light)
#    print(srf2.ranges)

    #srf.set_i2c_address(0xFC)

if __name__ == "__main__":
    test()
