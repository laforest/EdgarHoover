#! /usr/bin/python3

class Open_Interface:

    """
    Implements the sense and control parts of the OI spec.
    Does not use wait commands or iRobot scripting since it makes the
    robot unresponsive during.
    See: http://www.irobot.com/filelibrary/create/Create_Open_Interface_v6.pdf 
    """


    def __init__ (self, self.send_function, self.receive_function):
        self.send       = self.send_function
        self.receive    = self.receive_function

    def join(msb, lsb):
        return (msb << 8 | lsb)

    def saturate(value):
        return min(max(value, -65536), 65535)

    def split(value):
        value_lower = value & 0xFF
        value_upper = (value >> 8) & 0xFF
        return (value_upper, value_lower)

    def clip_and_split(value):
        return self.split(self.saturate(value))

    # Also returns to Passive mode
    def Start():
        return self.send([128])

    def Safe():
        return self.send([131])

    def Full():
        return self.send([132])

    def LEDs(Advance = 0, Play = 0, Power_Color = 0, Power_Intensity = 0):
        """
        0 = green, 255 = red
        """
        return self.send([139, (Advance << 3 | Play << 1), Power_Color, Power_Intensity])

    def Drive(velocity = 0, radius = 0):
        """
        Velocity goes from -32768 to 32767 -> -500 to 500 mm/s
        Radius goes from -32768 to 32767 -> -2000 to 2000 mm
        (Special cases: 32767 goes straight, -1/1 cw/ccw in-place)
        """
        (velocity_msb, velocity_lsb) = self.split(velocity)
        (radius_msb, radius_lsb) = self.split(radius)
        return self.send([137, velocity_msb, velocity_lsb, radius_msb, radius_lsb])

    def Drive_Direct(right_wheel = 0, left_wheel = 0):
        """
        Range: -32768 to 32767 -> -500 to 500 mm/s, positive values go forward
        """
        (left_wheel_msb, left_wheel_lsb) = self.split(left_wheel)
        (right_wheel_msb, right_wheel_lsb) = self.split(right_wheel)
        return self.send([145, right_wheel_msb, right_wheel_lsb, left_wheel_msb, left_wheel_lsb])

    def Digital_Outputs(pin_19 = 0 , pin_7 = 0 , pin_20 = 0):
        """
        NOTE: At turn-on, these go high for 3 seconds
        """
        return self.send([147, (pin_20 << 2 | pin_7 << 1 | pin_19)])

    def PWM_Low_Side_Drivers(pin_24 = 0, pin_22 = 0, pin_23 = 0):
        """
        NOTE: 0 to 100% DC -> 0 to 128
        """
        return self.send([144, pin_24, pin_22, pin_23])

    def Low_Side_Drivers(pin_24 = 0, pin_22 = 0, pin_23 = 0):
        """
        pin_22 and pin_23 can supply 0.5A, pin_24 can supply 1.5A
        Excess draw is limited and sets an overcurrent flag
        """
        return self.send([138, (pin_24 << 2 | pin_22 << 1 | pin_23)])

    def Send_IR(byte):
        """
        sent through pin_23, preload with 100Ohms in parallel with LED
        """
        return self.send([151, byte])

    def Song(song_number = 0, *args):
        args_list   = list(args)
        song_length = len(args_list) // 2
        return self.send([140, song_number, song_length].extend(args_list))

    def Play_Song(song_number = 0):
        """
        Does not work if a song currently plays. Check sensor packet.
        """
        return self.send([141, song_number])

    def Sensors():
        """
        Get all the data (52 bytes) by default (packet 6)
        """
        self.send([142, 6])
        return self.receive(52)

    if __name__ == "__main__":
        Start()
        Safe()
        for i in range(0, 256, 16):
            LEDs(Advance = 1, Play = 1, Power_Color = 255, Power_Intensity = i)
            sleep(0.05)
            LEDs(Advance = 0, Play = 0, Power_Color = 0, Power_Intensity = i)
            sleep(0.05)
        LEDs(Advance = 0, Play = 0, Power_Color = 0, Power_Intensity = 255)

