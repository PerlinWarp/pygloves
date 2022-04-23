# win32Pipe
# https://stackoverflow.com/questions/48542644/python-and-windows-named-pipes

import pywintypes
import struct
import time
import win32con
import win32file
import win32pipe


def encode(flexions, splay, joys, bools):
    """ Struct format is from: https://github.com/LucidVR/opengloves-driver/wiki/Driver-Input#opengloves-input-methods
    const std::array<std::array<float, 4>, 5> flexion; // Between 0 and 1
    const std::array<float, 5> splay; // Between 0 and 1
    const float joyX; // Between -1 and 1
    const float joyY; // Between -1 and 1
    const bool joyButton; // 0
    const bool trgButton; // 1
    const bool aButton;   // 2
    const bool bButton;   // 3
    const bool grab;      // 4
    const bool pinch;     // 5
    const bool menu;      // 6
    const bool calibrate; // 7
    
    const float trgValue; // between 0 - 1 
    """

    if splay is None:
        splay = [0.0] * 5

    if joys is None:
        joys = [0.0] * 2

    if bools is None:
        bools = [False] * 8

    # https://tuttlem.github.io/2016/04/06/packing-data-with-python.html
    packed_flexions = struct.pack('@20f', *flexions)
    packed_splays = struct.pack('@5f', *splay)
    packed_joys = struct.pack('@2f', *joys)
    packed_bools = struct.pack('@8?', *bools)
    packed_trg = struct.pack('@f', (flexions[4] + flexions[5] + flexions[6] + flexions[7]) / 4)

    return packed_flexions + packed_splays + packed_joys + packed_bools + packed_trg


class NamedPipe:
    def __init__(self, right_hand=True):
        if right_hand:
            # OpenGloves /named-pipe-communication-manager/src/DeviceProvider.cpp#L77
            self.pipe_name = r'\\.\pipe\vrapplication\input\glove\v2\right'

        else:
            self.pipe_name = r'\\.\pipe\vrapplication\input\glove\v2\left'

        try:
            # https://github.com/LucidVR/opengloves-driver/blob/develop/overlay/main.cpp#L128
            open_mode = win32con.GENERIC_READ | win32con.GENERIC_WRITE

            self.pipe = win32file.CreateFile(self.pipe_name,
                                        open_mode,
                                        0,  # no sharing
                                        None,  # default security
                                        win32con.OPEN_EXISTING,
                                        0,  # win32con.FILE_FLAG_OVERLAPPED,
                                        None)

            win32pipe.SetNamedPipeHandleState(self.pipe,
                                        win32pipe.PIPE_TYPE_BYTE | win32pipe.PIPE_READMODE_BYTE | win32pipe.PIPE_WAIT,
                                        None,
                                        None)


        except pywintypes.error:
            print("Pipe busy")
            time.sleep(0.1)
            self.__init__()

    def send(self, flexions, splay=None, joys=None, bools=None):
        encoded = encode(flexions, splay, joys, bools)
        win32file.WriteFile(self.pipe, encoded)


if __name__ == "__main__":
    ipc_right = NamedPipe(right_hand=True)
    ipc_left = NamedPipe(right_hand=False)

    try:
        for i1 in range(1, 10):

            for i2 in range(1, 10):

                for i3 in range(1, 10):

                    for i4 in range(1, 10):

                        for i5 in range(1, 10):

                            flexions = [i1/10, i1/10, i1/10, i1/10, i2/10, i2/10, i2/10, i2/10, i3/10, i3/10, i3/10, i3/10, i4/10, i4/10, i4/10, i4/10, i5/10, i5/10, i5/10, i5/10]

                            ipc_left.send(flexions)
                            ipc_right.send(flexions)

                            time.sleep(0.01)

                            print(f"Wrote {flexions} to IPC")

    except KeyboardInterrupt:
        print("Quitting")
        quit()
