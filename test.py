import sys
import serial

# data format: b0000_0000
# msb(left): axel (0: forward/backward, 1: right/left)
# other bits: b100_0000 = neutral, >b100_0000 = forward/right, <b100_0000 = backward/left

ser = serial.Serial('/dev/ttyACM1', 115200)    # TODO fix port

while True:
    c = input("use wasd to steer arduino, q to stop\n");
    if c == 'w':
        ser.write(b"\x7F")  # 0111_1111, full speed ahead!
    elif c == 's':
        ser.write(b"\x00")  # 0000_0000, abort mission!
    elif c == 'a':
        ser.write(b"\x80")  # 1000_0000, it's left o'clock!
    elif c == 'd':
        ser.write(b"\xFF")  # 1111_1111, take the third right!
    else:
        #ser.write(b"\x40")  # 0100_0000, neutral forward/backward
        ser.write(b"\x3C")
        #ser.write(b"\xC0")  # 1100_0000, neutral left/right
        ser.write(b"\x60")  # \0xBC