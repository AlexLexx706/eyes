import re
import threading
from types import SimpleNamespace
import time
import ctypes
import serial


# bit 0 - BUTTON_0 ... bit 8 - BUTTON_8
# bit 9 - BUTTON_END_LEFT
# bit 10 - BUTTON_END_RIGHT
# bit 11-12 - state of finger
# bit 13 - state of door


class ButtonState(ctypes.Structure):
    """Describe buttos states
    """
    _fields_ = (
        ("button_0", ctypes.c_int16, 1),
        ("button_1", ctypes.c_int16, 1),
        ("button_2", ctypes.c_int16, 1),
        ("button_3", ctypes.c_int16, 1),
        ("button_4", ctypes.c_int16, 1),
        ("button_5", ctypes.c_int16, 1),
        ("button_6", ctypes.c_int16, 1),
        ("button_7", ctypes.c_int16, 1),
        ("button_8", ctypes.c_int16, 1),
        ("button_end_left", ctypes.c_int16, 1),
        ("button_end_right", ctypes.c_int16, 1),
        ("finger_state", ctypes.c_int16, 2),
        ("door_state", ctypes.c_int16, 1),
    )
    _pack_ = 1


class BoxState(ctypes.Structure):
    """Describe box state
    """
    _fields_ = [
        # buttons states
        ("state", ButtonState),

        # position of finger 100..2500
        ("pos", ctypes.c_int16),

        # check sum (not used now)
        ("cs", ctypes.c_uint8),
    ]
    _pack_ = 1


class Protocol:
    """implementation of the protocol of interaction  between eyes controller and useless box controller
    """
    MAX_BUFFER_SIZE = 100

    def __init__(self):
        self._read_thread = None
        self._stop_event = threading.Event()
        self._serial = None
        self._cmd_index = 0
        self._re_header = re.compile(
            br'([A-Z]{2})([0-9A-F]{3})(?:%(\w*)%)?(.*)')
        self._state = ButtonState()
        self._cmd_condition = threading.Condition()
        self._last_re = SimpleNamespace(id='', prefix='', msg='')

    def start(self, port: str = '/dev/ttyUSB0', speed: int = 115200):
        """start protocol
        Args:
            port (str, optional): file path of port. Defaults to '/dev/ttyUSB0'.
            speed (int, optional): port speed
        """
        if self._read_thread is not None:
            raise RuntimeError('protocol already running')
        self._cmd_index = 0
        self._serial = serial.Serial(port, speed, timeout=1.0)
        self._read_thread = threading.Thread(target=self._read_proc)
        self._stop_event.clear()
        self._read_thread.start()

    def stop(self):
        """stop protocol
        """
        if self._read_thread is None:
            raise RuntimeError('Reading serial thread not exist')
        self._stop_event.set()
        self._read_thread.join()
        self._serial.close()
        self._read_thread = None

    def _send_cmd(self, cmd: str):
        """send command and waiting responce

        Args:
            cmd (_type_): _description_
        """
        cur_prefix = self._cmd_index
        self._cmd_index += 1
        full_cmd = f'%{cur_prefix}%{cmd}'
        # debug
        print(full_cmd)
        self._serial.write(f'{full_cmd}\n'.encode())
        self._wait_responce(cur_prefix)

    def _wait_responce(self, prefix: str, timeout: int = 0.5):
        with self._cmd_condition:
            self._cmd_condition.wait(timeout)
            if self._last_re.prefix != prefix:
                raise RuntimeWarning(
                    f"prefix:{prefix}!= {self._last_re.prefix} in:{self._last_re.id} msg:{self._last_re.msg}")

            if self._last_re.id == 'ER':
                raise RuntimeError(
                    f"error:{self._last_re.msg}")

    def set_mode(self, mode: int):
        """set current mode

        Args:
            mode (int): 0 - auto mode; 1 - manual
        """
        self._send_cmd(f'set,/par/mode,{mode}')

    def open_door(self):
        """send cmd open door
        """
        self._send_cmd('set,/par/manual/door,1')

    def close_door(self):
        """send cmd open door
        """
        self._send_cmd('set,/par/manual/door,0')

    def activate_state_stream(self):
        """activate state stream
        """
        self._send_cmd('em,state')

    def stop_state_stream(self):
        """stop state stream
        """
        self._send_cmd('dm,state')

    def set_finger_state(self, state: int):
        """move finger servo
        Args:
            state (int):
                0 - init state
                1 - ready state
                2 - pres state
        """
        self._send_cmd(f'set,/par/manual/finger,{state}')

    def move_finger(self, pos):
        """move finger to pos

        Args:
            pos (int): position of finger: 100...2500
        """
        self._send_cmd(f'set,/par/manual/pos,{pos}')

    def _read_proc(self):
        """decode stream form serial port
        """
        data = b''
        while not self._stop_event.is_set():
            line = self._serial.readline()
            data += line
            # only for debug
            print(repr(line))
            match = self._re_header.search(data)

            # header decoded
            if match:
                msg_id = match.group(1)
                msg_len = int(match.group(2), 16)

                # all data present
                if len(data) - match.start(4) >= msg_len:
                    start = match.start(4)
                    end = start + msg_len
                    # commands responce
                    if msg_id is ('RE', 'ER'):
                        msg_prefix = match.group(3)
                        # riase contition for waiter
                        with self._cmd_condition:
                            msg = data[start:end]
                            self._last_re.id = msg_id
                            self._last_re.prefix = msg_prefix
                            self._last_re.msg = msg
                            self._cmd_condition.notify()
                    # status message
                    elif msg_id == 'BS':
                        # update state
                        self._state = ButtonState.from_buffer_copy(
                            data[start:end])
                    # cut data
                    data = data[end:]

            # cut unknown data
            if len(data) > self.MAX_BUFFER_SIZE:
                data = data[-self.MAX_BUFFER_SIZE:]


if __name__ == '__main__':
    protocol = Protocol()
    protocol.start(port='/dev/ttyUSB0')
    time.sleep(5)
    protocol.set_mode(1)
    protocol.activate_state_stream()
    time.sleep(10)
    protocol.open_door()
    time.sleep(1)
    protocol.close_door()
    time.sleep(1)
    protocol.set_finger_state(1)
    time.sleep(2)
    protocol.set_finger_state(2)
    time.sleep(2)
    protocol.set_finger_state(0)
    time.sleep(2)
    protocol.move_finger(100)
    time.sleep(2)
    protocol.move_finger(2000)
    time.sleep(2)
    protocol.stop_state_stream()
    time.sleep(2)
    protocol.stop()
