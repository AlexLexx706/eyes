import threading
import time
import ctypes
import serial


class Protocol:
    """implementation of the protocol of interaction  between eyes controller and useless box controller
    """

    def __init__(self):
        self._read_thread = None
        self._stop_event = threading.Event()
        self._serial = None
        self._cmd_index = 0

    def start(self, port:str='/dev/ttyUSB0', speed:int=115200):
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

    def _send_cmd(self, cmd:str):
        """send command and waiting responce

        Args:
            cmd (_type_): _description_
        """
        cur_prefix = self._cmd_index
        self._cmd_index += 1
        full_cmd = f'%{cur_prefix}%{cmd}'
        print(full_cmd)
        self._serial.write(f'{full_cmd}\n'.encode())
        self._wait_responce(cur_prefix)
    
    def _wait_responce(self, prefix:str):
        return 

    def set_mode(self, mode:int):
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

    def set_finger_state(self, state:int):
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
        while not self._stop_event.is_set():
            symbol = self._serial.readline()
            print(symbol)

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
