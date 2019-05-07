#! /usr/bin/python3

import Communication_Interfaces
import Open_Interface
import SRF08
from time import sleep
import os

def robot_status(OI, SRL, SRR):
    SRL.do_ranging()
    SRL.read_light()
    SRL.read_ranges()
    print("SRL light: {0} Ranges: {1}".format(SRL.light, SRL.ranges))

    SRR.do_ranging()
    SRR.read_light()
    SRR.read_ranges()
    print("SRR light: {0} Ranges: {1}".format(SRR.light, SRR.ranges))

    OI.Get_All_Sensors()
    print("Bumps L R: {0} {1}".format(OI.Bump_Left(), OI.Bump_Right()))

if __name__ == "__main__":
    CI  = Communication_Interfaces()

    OI  = Open_Interface(CI.uart_read, CI.uart_write)
    OI.Start()
    OI.Full()

    SRL = SRF08(CI.i2c_read, CI.i2c_write, 0x72)
    SRL.set_gain(31)
    SRL.set_range(255)

    SRR = SRF08(CI.i2c_read, CI.i2c_write, 0x76)
    SRR.set_gain(31)
    SRR.set_range(255)

    while (True):
        robot_status(OI, SRL, SRR)
        sleep(1)
        os.system('clear')

