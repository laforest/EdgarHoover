#! /usr/bin/python3

"""
Common Functions
"""

import serial

def Init_Port(name, baudrate = 57600):
    port = serial.Serial(port     = name,
                         baudrate = baudrate,
                         bytesize = serial.EIGHTBITS,
                         parity   = serial.PARITY_NONE,
                         stopbits = serial.STOPBITS_ONE,
                         xonxoff  = False,
                         timeout  = None) # What if Create hangs, but not brain?
    def send(byte_list):
        return port.write(bytes(byte_list))

    def receive(bytes_count):
        return port.read(bytes_count)
    return (send, receive)

def join(msb, lsb):
    return (msb << 8 | lsb)

def saturate(value):
    return min(max(value, -65536), 65535)

def split(value):
    value_lower = value & 0xFF
    value_upper = (value >> 8) & 0xFF
    return (value_upper, value_lower)

def clip_and_split(value):
    return split(saturate(value))

