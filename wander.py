#! /usr/bin/python3

from Communication_Interfaces   import Communication_Interfaces
from Open_Interface             import Open_Interface
from SRF08                      import SRF08
from time                       import sleep
import os
import sys

def wander (OI, SRL, SRR):
    SRL.do_ranging()
    SRR.do_ranging()
    OI.Get_All_Sensors()

    nearest_left    = SRL.ranges[0]
    nearest_right   = SRR.ranges[0]
 
    next_nearest_left    = SRL.ranges[1]
    next_nearest_right   = SRR.ranges[1]

    left        = next_nearest_right - (next_nearest_right - nearest_right)
    right       = next_nearest_left  - (next_nearest_left  - nearest_left)

    print(nearest_left, nearest_right, next_nearest_left, next_nearest_right, left, right)

    OI.Drive_Direct(left, right)

#    print("SRL light: {0}\tRanges: {1}".format(SRL.light, SRL.ranges))
#    print("SRR light: {0}\tRanges: {1}".format(SRR.light, SRR.ranges))
#    print("Bumps L R: {0} {1}".format(OI.Bump_Left(), OI.Bump_Right())
#    print("Wheeldrop L R C: {0} {1} {2}".format(OI.Wheeldrop_Left(), OI.Wheeldrop_Right(), OI.Wheeldrop_Caster())
#    print("Wall Seen: {0}".format(OI.Wall_Seen())
#    print("Cliff Seen L FL FR R: {0} {1} {2} {3}".format(OI.Cliff_Seen_Left(), OI.Cliff_Seen_Front_Left(), OI.Cliff_Seen_Front_Right(), OI.Cliff_Seen_Right())
#    print("Virtual Wall Seen: {0}".format(OI.Virtual_Wall_Seen())
#    print("Overcurrent LSD0 LSD1 LSD2 LW RW: {0} {1} {2} {3} {4}".format(OI.Overcurrent_LSD0(), OI.Overcurrent_LSD1(), OI.Overcurrent_LSD2(), OI.Overcurrent_Left_Wheel(), OI.Overcurrent_Right_Wheel())
#    print("IR Byte: {0}".format(OI.IR_Byte())
#    print("Buttons Advance Play: {0} {1}".format(OI.Button_Play_Pressed(), OI.Button_Advance_Pressed())
#    print("Last Distance Angle: {0} {1}".format(OI.Last_Distance(), OI.Last_Angle())
#    print("Charging State: {0}".format(OI.Charging_State())
#    print("Battery Voltage Current Temp Charge Capacity: {0} {1} {2} {3} {4}".format(OI.Battery_Voltage(), OI.Battery_Current(), OI.Battery_Temperatur(), OI.Battery_Charge(), OI.Battery_Capacity()))
#    print("Wall Signal: {0}".format(OI.Wall_Signal()))
#    print("Cliff Signal L FL FR R: {0} {1} {2} {3}".format(OI.CLiff_Left_Signal(), OI.Cliff_Front_Left_Signal(), OI.Cliff_Front_Right_Signal(), OI.Cliff_Right_Signal()))
#    print("Charging HomeBase Internal: {0} {1}".format(OI.Charging_Home_Base(), OI.Charging_Internal()))
#    print("OI Mode: {0}".format(OI.OI_Mode()))
#    print("Last DriveVel DriveRad RightVel LeftVel: {0} {1} {2} {3}".format(OI.Last_Drive_Velocity(), OI.Last_Drive_Radius(), OI.Last_Right_Velocity(), OI.Last_Left_Velocity()))

if __name__ == "__main__":
    CI  = Communication_Interfaces()
    OI  = Open_Interface(CI.uart_read, CI.uart_write)
    SRL = SRF08(CI.i2c_read, CI.i2c_write, 0x72)
    SRR = SRF08(CI.i2c_read, CI.i2c_write, 0x76)

    while (True):
        wander(OI, SRL, SRR)
        if (OI.Wheeldrop_Caster() == True):
            OI.Start()
            sys.exit()

