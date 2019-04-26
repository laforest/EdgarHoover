#! /usr/bin/python3

from USB_ISS import USB_ISS

import time

def test ():
    iss = USB_ISS()
    iss.set_i2c_serial_mode()
    print()
    while True:
        time.sleep(1)
        data = iss.uart_read(15)
        print(data)
        data = [0x65] * 15
        iss.uart_write(data)

if __name__ == "__main__":
    test()
