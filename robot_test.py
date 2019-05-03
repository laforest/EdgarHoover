#! /usr/bin/python3

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
    OI = Open_Interface()
    test(OI)

