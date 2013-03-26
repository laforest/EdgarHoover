#! /usr/bin/python3

import robot_common as rc

(send, receive) = rc.Init_Port(port_name = '/dev/ttyUSB0')

# Also returns to Passive mode
def Start():
    return send([128])

def Safe():
    return send([131])

def Full():
    return send([132])

# 0 = green, 255 = red
def LEDs(Advance = 0, Play = 0, Power_Color = 0, Power_Intensity = 0):
    return send([139, (Advance << 3 | Play << 1), Power_Color, Power_Intensity])

# NOTE: Velocity goes from -32768 to 32767 -> -500 to 500 mm/s
#       Radius goes from -32768 to 32767 -> -2000 to 2000 mm
#       (Special cases: 32767 goes straight, -1/1 cw/ccw in-place)
def Drive(velocity = 0, radius = 0):
    (velocity_msb, velocity_lsb) = rc.split(velocity)
    (radius_msb, radius_lsb) = rc.split(radius)
    return send([137, velocity_msb, velocity_lsb, radius_msb, radius_lsb])

# Range: -32768 to 32767 -> -500 to 500 mm/s, positive values go forward
def Drive_Direct(right_wheel = 0, left_wheel = 0):
    (left_wheel_msb, left_wheel_lsb) = rc.split(left_wheel)
    (right_wheel_msb, right_wheel_lsb) = rc.split(right_wheel)
    return send([145, right_wheel_msb, right_wheel_lsb, left_wheel_msb, left_wheel_lsb])

# NOTE: At turn-on, these go high for 3 seconds
def Digital_Outputs(pin_19 = 0 , pin_7 = 0 , pin_20 = 0):
    return send([147, (pin_20 << 2 | pin_7 << 1 | pin_19)])

# NOTE: 0 to 100% DC -> 0 to 128
def PWM_Low_Side_Drivers(pin_24 = 0, pin_22 = 0, pin_23 = 0):
    return send([144, pin_24, pin_22, pin_23])

# NOTE: pin_22 and pin_23 can supply 0.5A, pin_24 can supply 1.5A
#       Excess draw is limited and sets an overcurrent flag
def Low_Side_Drivers(pin_24 = 0, pin_22 = 0, pin_23 = 0):
    return send([138, (pin_24 << 2 | pin_22 << 1 | pin_23)])

# sent through pin_23, preload with 100Ohms in parallel with LED
def Send_IR(byte):
    return send([151, byte])

def Song(song_number = 0, *args):
    args_list   = list(args)
    song_length = len(args_list) // 2
    return send([140, song_number, song_length].extend(args_list))

# Does not work if a song currently plays. Check sensor packet.
def Play_Song(song_number = 0):
    return send([141, song_number])

# Get all the data (52 bytes) by default (packet 6)
def Sensors():
    send([142, 6])
    return receive(52)

if __name__ == "__main__":
    Start()
    Safe()

    for i in range(0, 256, 16):
        LEDs(Advance = 1, Play = 1, Power_Color = 255, Power_Intensity = i)
        sleep(0.05)
        LEDs(Advance = 0, Play = 0, Power_Color = 0, Power_Intensity = i)
        sleep(0.05)
    LEDs(Advance = 0, Play = 0, Power_Color = 0, Power_Intensity = 255)

