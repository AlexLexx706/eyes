import serial
#Serial takes these two parameters: serial device and baudrate
with serial.Serial('/dev/ttyUSB0', 115200) as ser:
    while 1:
        res = ser.read_until()
        state = int.from_bytes(res[:2], 'little')
        print(bin(state))
