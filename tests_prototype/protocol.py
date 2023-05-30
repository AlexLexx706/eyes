import threading
import time
import ctypes
import enum
import serial


class Cmd(enum.IntEnum):
    """set of cmd
    """
    OPEN_DOOR = 1
    CLOSE_DOOR = 2
    PRESS_BUTTON = 3
    MOVE_SERVO = 4
    MOVE_FINGER = 5
    ACTIVATE_STATE_STREAM = 6
    STOP_STATE_STREAM = 7


class CmdHead(ctypes.Structure):
    """describe header of packet
    """

    _fields_ = [
        ("begin", ctypes.c_int8),
        ("size", ctypes.c_uint8),
    ]
    _pack_ = 1


class CmdWithoutParams(ctypes.Structure):
    """describe packet of cmd
    """
    _fields_ = [
        ('head', CmdHead),
        ("cmd", ctypes.c_uint8),
        ('crc', ctypes.c_uint8)
    ]
    _pack_ = 1


class CmdMoveServo(ctypes.Structure):
    """describe packet Move servo:
        parameters:
            num (c_uint8): number of servo: 0 - finger servo, 1 - door servo
            value (c_uint8) - value of servo 0 (min) - 255 (max)
    Args:
        ctypes (_type_): _description_
    """
    _fields_ = [
        ('head', CmdHead),
        ("cmd", ctypes.c_uint8),
        ("num", ctypes.c_uint8),
        ("value", ctypes.c_uint8),
        ('crc', ctypes.c_uint8)
    ]
    _pack_ = 1


class CmdMoveFinger(ctypes.Structure):
    """describe packet Move finger, move finger to button:
    Args:
        ctypes (_type_): _description_
    """
    _fields_ = [
        ('head', CmdHead),
        ("cmd", ctypes.c_uint8),
        ("btn", ctypes.c_uint8),
        ('crc', ctypes.c_uint8)
    ]
    _pack_ = 1


class Protocol:
    """implementation of the protocol of interaction  between eyes controller and useless box controller
    """

    def __init__(self):
        self._state = 0
        self._read_thread = None
        self._stop_flag = False
        self._serial = None

    @staticmethod
    def fast_crc8(data):
        """calculate fast crc 8 for data
        Args:
            data (bytes): data for calculation crc 8
        Returns:
            int: crc 8 bit
        """
        res = 0
        for val in data:
            res = 0xff & ((res << 2) | (res >> 6)) ^ val
        return 0xff & ((res << 2) | (res >> 6))

    def start(self, port='/dev/ttyUSB0'):
        """start protocol
        Args:
            port (str, optional): file path of port. Defaults to '/dev/ttyUSB0'.
        """
        if self._read_thread is not None:
            raise RuntimeError('protocol already running')
        self._serial = serial.Serial(port, 115200, timeout=1.0)
        self._read_thread = threading.Thread(target=self._read_serial)
        self._stop_flag = False
        self._read_thread.start()

    def stop(self):
        """stop protocol
        """
        if self._read_thread is None:
            raise RuntimeError('Reading serial thread not exist')
        self._stop_flag = True
        self._read_thread.join()
        self._serial.close()
        self._read_thread = None

    def send_cmd(self, cmd):
        """send command without params

        Args:
            cmd (Cmd): cmd
        """
        packet = CmdWithoutParams()
        packet.head.begin = ord('x')
        packet.head.size = 1
        packet.cmd = cmd
        packet.crc = self.fast_crc8(bytes(packet)[:-1])
        self._serial.write(bytes(packet))

    def open_door(self):
        """send cmd open door
        """
        self.send_cmd(Cmd.OPEN_DOOR)

    def close_door(self):
        """send cmd open door
        """
        self.send_cmd(Cmd.CLOSE_DOOR)

    def activate_state_stream(self):
        """activate state stream
        """
        self.send_cmd(Cmd.ACTIVATE_STATE_STREAM)

    def stop_state_stream(self):
        """stop state stream
        """
        self.send_cmd(Cmd.STOP_STATE_STREAM)

    def move_servo(self, num, value):
        """move servo

        Args:
            num (int): servo num: 0 - finger, 1 - door servo
            value (int): value 0 - min value, 255 - max value
        """
        packet = CmdMoveServo()
        packet.head.begin = ord('x')
        packet.head.size = ctypes.sizeof(CmdMoveServo) - 3
        packet.cmd = Cmd.MOVE_SERVO
        packet.num = num
        packet.value = value
        packet.crc = self.fast_crc8(bytes(packet)[:-1])
        self._serial.write(bytes(packet))

    def move_finger(self, btn):
        """move finger to button

        Args:
            btn (int): button number 0 - 8
        """
        packet = CmdMoveFinger()
        packet.head.begin = ord('x')
        packet.head.size = ctypes.sizeof(CmdMoveFinger) - 3
        packet.cmd = Cmd.MOVE_FINGER
        packet.btn = btn
        packet.crc = self.fast_crc8(bytes(packet)[:-1])
        self._serial.write(bytes(packet))

    def press_btn(self, btn):
        """press btn

        Args:
            btn (int): button number 0 - 8
        """
        packet = CmdMoveFinger()
        packet.head.begin = ord('x')
        packet.head.size = ctypes.sizeof(CmdMoveFinger) - 3
        packet.cmd = Cmd.PRESS_BUTTON
        packet.btn = btn
        packet.crc = self.fast_crc8(bytes(packet)[:-1])
        self._serial.write(bytes(packet))

    def _read_serial(self):
        while not self._stop_flag:
            res = self._serial.read(3)
            print(res)
            # if res:
            #     print(f'res:{res}, len:{len(res)}')
            #     self._state = int.from_bytes(res[:2], 'little')
            #     print(bin(self._state))


protocol = Protocol()
protocol.start(port='/dev/ttyUSB0')
time.sleep(1)
protocol.open_door()
time.sleep(1)
protocol.close_door()
time.sleep(1)
protocol.move_servo(0, 10)
time.sleep(2)
protocol.move_servo(1, 100)
time.sleep(2)
protocol.move_finger(1)
time.sleep(2)
protocol.press_btn(3)
time.sleep(2)
protocol.activate_state_stream()
time.sleep(2)
protocol.stop_state_stream()
time.sleep(2)
protocol.stop()


# print(create_cmd_without_params_packet(Cmd.OpenDoor))
