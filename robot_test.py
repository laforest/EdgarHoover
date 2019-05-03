#! /usr/bin/python3

from USB_ISS        import USB_ISS
from Open_Interface import Open_Interface
from time           import sleep

def test (OI):
    OI.Start()
    OI.Full()
    OI.LEDs(0,0,0,0)
    sleep(2)
    OI.LEDs(1,1,255,255)
    sleep(2)
    OI.LEDs(0,0,0,0)
    OI.Start()

if __name__ == "__main__":
    UI = USB_ISS()
    OI = Open_Interface(UI.uart_write, UI.uart_read)
    test(OI)

