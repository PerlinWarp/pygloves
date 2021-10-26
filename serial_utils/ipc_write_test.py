# win32Pipe
'''
https://stackoverflow.com/questions/48542644/python-and-windows-named-pipes
'''
import struct, time
import win32pipe, win32file, win32con 
from win32security import *
from ntsecuritycon import *
from win32process import *

def pack_struct(flexion):
    ''' Struct format is from: https://github.com/LucidVR/opengloves-driver/.../EncodingManager.h#L17
  const std::array<float, 5> flexion;
  const float joyX;
  const float joyY;
  const bool joyButton;
  const bool trgButton;
  const bool aButton;
  const bool bButton;
  const bool grab;
  const bool pinch;
  const bool menu;
  const bool calibrate;
    '''
    joyX = 512
    joyY = 512
    bools = [False]*8

    # https://tuttlem.github.io/2016/04/06/packing-data-with-python.html
    pack_obj = struct.pack('@5f', flexion[0], flexion[1], flexion[2], flexion[3], flexion[4])
    joys = struct.pack('@2f', joyX, joyY)
    pack_bools = struct.pack('@8?', *bools)
    pack_obj = pack_obj + joys + pack_bools
    return pack_obj

def pipe_security():
    dacl = ACL()

    # Deny NT AUTHORITY\NETWORK SID
    sid = CreateWellKnownSid(WinNetworkSid)
    dacl.AddAccessDeniedAce(ACL_REVISION, GENERIC_ALL, sid)

    # Allow current user SID
    token = OpenProcessToken(GetCurrentProcess(), TOKEN_QUERY)
    sid = GetTokenInformation(token, TokenUser)[0]
    dacl.AddAccessAllowedAce(ACL_REVISION, GENERIC_READ | GENERIC_WRITE, sid)

    security_descriptor = SECURITY_DESCRIPTOR()
    security_descriptor.SetSecurityDescriptorDacl(True, dacl, False)

    security_attributes = SECURITY_ATTRIBUTES()
    security_attributes.SECURITY_DESCRIPTOR = security_descriptor
    return security_attributes

if __name__ == "__main__":
    fingers = [0,512,512,512,1023]
    packed = pack_struct(fingers)

    # pipename should be of the form \\.\pipe\mypipename
    # OpenGloves /named-pipe-communication-manager/src/DeviceProvider.cpp#L77
    pipename = r'\\.\\pipe\\vrapplication\\input\\right'
    #pipename = "\\\\.\\pipe\\vrapplication\\input\\left"

    #security_attributes = pipe_security()
    # https://github.com/LucidVR/opengloves-driver/blob/develop/overlay/main.cpp#L128
    open_mode = win32con.GENERIC_READ | win32con.GENERIC_WRITE

    pipe = win32file.CreateFile(pipename,
                                     open_mode,
                                     0, # no sharing
                                     None, # default security
                                     win32con.OPEN_EXISTING,
                                     0, # win32con.FILE_FLAG_OVERLAPPED,
                                     None)
    try:
        #win32pipe.ConnectNamedPipe(pipe, None)
        #print("Connected")

        for i in range(0,10):
            fingers = [i]*5
            packed_data = pack_struct(fingers)
            win32file.WriteFile(pipe, packed_data)
            time.sleep(0.01)
            print(f"Wrote {i} to IPC")
    except KeyboardInterrupt:
        print("Quitting")
        win32file.CloseHandle(pipe)
        quit()
    finally:
        win32file.CloseHandle(pipe)