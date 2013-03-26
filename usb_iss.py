#! /usr/bin/python3

"""
Implements the I2C functionality of the Devantech USB-ISS module
You can adapt this code for SPI/UART/IO etc... modes
See: http://robot-electronics.co.uk/htm/usb_iss_tech.htm
"""

import robot_common as rc

USB_ISS         = 0x5A
ISS_MODE        = 0x02
IO_MODE         = 0xAA # All IO as digital input (10101010)
I2C_H_100KHZ    = 0x60
I2C_H_400KHZ    = 0x70
I2C_AD1         = 0x55

# Shows up as a UART. Edit to correct device name
(send, receive) = rc.Init_Port('/dev/tty.usbmodem00005251')

def ACK():
    """
    Just check the first return byte.
    Short of a defective module, any error is from a bad command.
    """
    ack_nack = receive(2)
    if ack_nack[0] == 0xFF:
        return True
    return False

def I2C_Init():
    send([USB_ISS, ISS_MODE, I2C_H_100KHZ, IO_MODE])
    return ACK() 

def I2C_Write(address, register, count, data):
    """
    Send 60 data bytes max so as not to overflow the internal buffer.
    """
    send([I2C_AD1, address, register, count] + data)
    if receive(1) == 0x00:
        return False
    return True

def I2C_Read(address, register, count):
    """
    Read 60 data bytes max so as not to underflow the internal buffer.
    Don't pre-add the read bit, we do that.
    """
    send([I2C_AD1, address+1, register, count])
    return receive(count)


