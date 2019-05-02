#! /usr/bin/python3

# To convert bytes into signed/unsigned ints, depending on byte data format.
from struct import unpack

class Open_Interface:

    """
    Implements the sense and control parts of the OI spec.
    Does not use wait commands or iRobot scripting since it makes the
    robot unresponsive during.
    See: http://www.irobot.com/filelibrary/create/Create_Open_Interface_v6.pdf (gone)
         https://www.manualslib.com/manual/396738/Irobot-Create-Open-Interface.html
    """


    def __init__ (self, self.send_function, self.receive_function):
        self.send       = self.send_function
        self.receive    = self.receive_function
        self.sensors    = bytearray()

    def join(msb, lsb):
        return (msb << 8 | lsb)

    def split(value):
        value_lower = value & 0xFF
        value_upper = (value >> 8) & 0xFF
        return (value_upper, value_lower)

    def Start (self):
        """MUST send this command first before any other. Also returns to Passive mode."""
        return self.send([128])

    def Safe (self):
        return self.send([131])

    def Full (self):
        return self.send([132])

    def LEDs (self, Advance = 0, Play = 0, Power_Color = 0, Power_Intensity = 0):
        """0 = green, 255 = red"""
        return self.send([139, (Advance << 3 | Play << 1), Power_Color, Power_Intensity])

    def Drive (self, velocity = 0, radius = 0):
        """
        Velocity goes from -500 to 500 mm/s
        Radius goes from -2000 to 2000 mm (robot center to turn center)
        (Special cases: 32767 or 32768 goes straight, -1/1 turns cw/ccw in-place)
        """
        (velocity_msb, velocity_lsb) = self.split(velocity)
        (radius_msb, radius_lsb) = self.split(radius)
        return self.send([137, velocity_msb, velocity_lsb, radius_msb, radius_lsb])

    def Drive_Direct (self, right_wheel = 0, left_wheel = 0):
        """Range: -32768 to 32767 -> -500 to 500 mm/s, positive values go forward"""
        (left_wheel_msb, left_wheel_lsb) = self.split(left_wheel)
        (right_wheel_msb, right_wheel_lsb) = self.split(right_wheel)
        return self.send([145, right_wheel_msb, right_wheel_lsb, left_wheel_msb, left_wheel_lsb])

    def Digital_Outputs (self, pin_19 = 0 , pin_7 = 0 , pin_20 = 0):
        """NOTE: At turn-on, these go high for 3 seconds"""
        return self.send([147, (pin_20 << 2 | pin_7 << 1 | pin_19)])

    def PWM_Low_Side_Drivers (self, pin_24 = 0, pin_22 = 0, pin_23 = 0):
        """NOTE: 0 to 100% DC -> 0 to 128"""
        return self.send([144, pin_24, pin_22, pin_23])

    def Low_Side_Drivers (self, pin_24 = 0, pin_22 = 0, pin_23 = 0):
        """
        pin_22 and pin_23 can supply 0.5A, pin_24 can supply 1.5A
        Excess draw is limited and sets an overcurrent flag
        """
        return self.send([138, (pin_24 << 2 | pin_22 << 1 | pin_23)])

    def Send_IR (self, byte):
        """sent through pin_23, preload with 100Ohms in parallel with LED"""
        return self.send([151, byte])

    def Song (self, song_number = 0, *args):
        args_list   = list(args)
        song_length = len(args_list) // 2
        return self.send([140, song_number, song_length].extend(args_list))

    def Play_Song (self, song_number = 0):
        """Does not work if a song currently plays. Check sensor packet."""
        return self.send([141, song_number])

    def Get_All_Sensors (self):
        """Get all the sensor data (52 bytes in packet 6)"""
        self.send([142, 6])
        raw_sensors = self.receive(52)

    # Must use slices even for single bytes else they convert to ints prematurely.

    def Bump_Right (self):
        return unpack('B', self.sensors[0:1]) & 0x1

    def Bump_Left (self):
        return (unpack('B', self.sensors[0:1]) & 0x2) >> 1

    def Wheeldrop_Right (self):
        return (unpack('B', self.sensors[0]) & 0x4) >> 2

    def Wheeldrop_Left (self):
        return (unpack('B', self.sensors[0]) & 0x8) >> 3

    def Wheeldrop_Caster (self):
        return (unpack('B', self.sensors[0:1]) & 0x10) >> 4

    def Wall_Seen (self):
        return unpack('?', self.sensors[1:2])

    def Cliff_Seen_Left (self):
        return unpack('?', self.sensors[2:3])

    def Cliff_Seen_Front_Left (self):
        return unpack('?', self.sensors[3:4])

    def Cliff_Seen_Front_Right (self):
        return unpack('?', self.sensors[4:5])

    def Cliff_Seen_Right (self):
        return unpack('?', self.sensors[5:6])

    def Virtual_Wall_Seen (self):
        return unpack('?', self.sensors[6:7])

    def Overcurrent_LSD0 (self):
        """Low Side Driver 0, 0.5A"""
        return unpack('B', self.sensors[7:8]) & 0x1

    def Overcurrent_LSD1 (self):
        """Low Side Driver 1, 0.5A"""
        return (unpack('B', self.sensors[7:8]) & 0x2) >> 1

    def Overcurrent_LSD2 (self):
        """Low Side Driver 2, 1.6A"""
        return (unpack('B', self.sensors[7:8]) & 0x4) >> 2

    def Overcurrent_Right_Wheel (self):
        """1.0A"""
        return (unpack('B', self.sensors[7:8]) & 0x8) >> 3

    def Overcurrent_Left_Wheel (self):
        """1.0A"""
        return (unpack('B', self.sensors[7:8]) & 0x10) >> 4

    # Bytes 8 and 9 are always 0 (packet 15 and 16)

    def IR_Byte (self):
        """See Open Interface doc, pg.18, for meaning of byte"""
        return unpack('B', self.sensors[10:11])

    def Button_Play_Pressed (self):
        return unpack('B', self.sensors[11:12]) & 0x1

    def Button_Advance_Pressed (self):
        return (unpack('B', self.sensors[11:12]) & 0x4) >> 2

    def Last_Distance (self):
        """Distance travelled since last call to this function. Capped to +/-32k mm."""
        return unpack('h', self.sensors[12:14])

    def Last_Angle (self):
        """Angle turned since last call to this function. Capped to +/-32k degrees. CCW positive, CW negative."""
        return unpack('h', self.sensors[14:16])

    def Charging_State (self):
        """
        0 Not charging
        1 Reconditioning Charging
        2 Full Charging
        3 Trickle Charging
        4 Waiting
        5 Charging Fault Condition
        """
        return unpack('B', self.sensors[16:17])

    def Battery_Voltage (self):
        """0-64k mV"""
        return unpack('H', self.sensors[17:19])

    def Battery_Current (self):
        """+/-32k mA, negative is discharging, positive is charging"""
        return unpack('H', self.sensors[19:21])

    def Battery_Temperature (self):
        """+/-128 degC"""
        return unpack('b', self.sensors[21:22])

    def Battery_Charge (self)
        """Estimated current battery charge: 0-64k mAh"""
        return unpack('H', self.sensors[22:24])

    def Battery_Capacity (self)
        """Estimated current battery capacity: 0-64k mAh"""
        return unpack('H', self.sensors[24:26])

    def Wall_Signal (self):
        """Wall sensor. 0-4k"""
        return unpack('H', self.sensors[26:28]) 

    def Cliff_Left_Signal (self):
        """Left cliff sensor. 0-4k"""
        return unpack('H', self.sensors[28:30]) 

    def Cliff_Front_Left_Signal (self):
        """Front left cliff sensor. 0-4k"""
        return unpack('H', self.sensors[30:32]) 

    def Cliff_Front_Right_Signal (self):
        """Front right cliff sensor. 0-4k"""
        return unpack('H', self.sensors[32:34]) 

    def Cliff_Right_Signal (self):
        """Right cliff sensor. 0-4k"""
        return unpack('H', self.sensors[34:36]) 

    # Skipped implementing the digital (byte 36) and analog (bytes 37-38) I/O pins here.

    def Charging_Home_Base (self):
        return (unpack('B', self.sensors[39:40]) & 0x2) >> 1

    def Charging_Internal (self):
        return (unpack('B', self.sensors[39:40]) & 0x1)

    def OI_Mode (self):
        """
        0 Off
        1 Passive
        2 Safe
        3 Full
        """
        return unpack('B', self.sensors[40:41])

    # Skipped remaining commands (song status/number, last requested radius/velocities)

