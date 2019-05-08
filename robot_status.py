#! /usr/bin/python3

from Communication_Interfaces   import Communication_Interfaces
from Open_Interface             import Open_Interface
from SRF08                      import SRF08
from time                       import sleep
import os

def robot_status(OI, SRL, SRR):
    SRL.do_ranging()
    SRR.do_ranging()
    OI.Get_All_Sensors()
    bump_left  = OI.Bump_Left()
    bump_right = OI.Bump_Right()

    print("SRL light: {0}\tRanges: {1}".format(SRL.light, SRL.ranges))
    print("SRR light: {0}\tRanges: {1}".format(SRR.light, SRR.ranges))
    print("Bumps L R: {0} {1}".format(bump_left, bump_right))

if __name__ == "__main__":
    CI  = Communication_Interfaces()
    OI  = Open_Interface(CI.uart_read, CI.uart_write)
    SRL = SRF08(CI.i2c_read, CI.i2c_write, 0x72)
    SRR = SRF08(CI.i2c_read, CI.i2c_write, 0x76)

    os.system('clear')
    while (True):
        robot_status(OI, SRL, SRR)
        sleep(1)
        os.system('clear')

