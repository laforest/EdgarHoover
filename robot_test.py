#! /usr/bin/python3

from Communication_Interfaces   import Communication_Interfaces
from Open_Interface             import Open_Interface
from time                       import sleep

def test (OI):
    OI.Start()
    OI.Full()

    OI.LEDs(0, 0, 255, 255)
    OI.Drive(500, 1)
    sleep(2)

    OI.LEDs(0, 1, 127, 255)
    OI.Drive(0, 0)
    sleep(2)

    OI.LEDs(1, 1, 0, 255)
    OI.Drive(500, -1)
    sleep(2)

    OI.LEDs(1, 0, 0, 0)
    OI.Drive(0, 0)

    OI.Start()

if __name__ == "__main__":
    CI = Communication_Interfaces()
    OI = Open_Interface(CI.uart_write, CI.uart_read)
    test(OI)

