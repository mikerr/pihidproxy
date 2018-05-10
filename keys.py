import evdev
from evdev import InputDevice, categorize, ecodes
dev = InputDevice('/dev/input/event0')

NULL_CHAR = chr(0)

def write_report(report):
    with open('/dev/hidg0', 'rb+') as fd:
        fd.write(report.encode())

scancodes = {
    # Scancode: ASCIICode
    0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
    10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
    20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
    30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
    40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
    50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 57: u' ', 100: u'RALT'
}

#grab provides exclusive access to the device
dev.grab()

caps= False;
hidkey =0

#loop
for event in dev.read_loop():
    if event.type == ecodes.EV_KEY:
        data = categorize(event)
        if data.scancode == 42:
            if data.keystate == 1:
                caps = True
            if data.keystate == 0:
                caps = False
        if data.keystate == 1:  # Down events only
            key_lookup = u'{}'.format(scancodes.get(data.scancode))

            print key_lookup, data.scancode

            if len(key_lookup) == 1 :
               hidkey = ord(key_lookup) - 93 # a-z
            if hidkey < 0: # 1-9
                   hidkey += 74

            if data.scancode == 57: hidkey = 44 # space
            if data.scancode == 14: hidkey = 42 # bkspc
            if data.scancode == 28: hidkey = 40 # enter
            if data.scancode == 2: hidkey = 41 # ESC

            if data.scancode == 106: hidkey = 79 # RIGHT
            if data.scancode == 105: hidkey = 80 # LEFT
            if data.scancode == 108: hidkey = 81 # DOWN
            if data.scancode == 103: hidkey = 82 # UP

            if data.scancode == 59: hidkey = 58 # F1
            if data.scancode == 60: hidkey = 59 # F2
            if data.scancode == 61: hidkey = 60 # F3
            if data.scancode == 62: hidkey = 61 # F4
            if data.scancode == 63: hidkey = 62 # F5
            if data.scancode == 64: hidkey = 63 # F6
            if data.scancode == 65: hidkey = 64 # F7
            if data.scancode == 66: hidkey = 65 # F8
            if data.scancode == 67: hidkey = 66 # F9
            if data.scancode == 68: hidkey = 67 # F10
            if data.scancode == 69: hidkey = 68 # F11
            if data.scancode == 70: hidkey = 69 # F12


            if data.scancode == 26: hidkey = 45 # -

            print key_lookup, data.scancode, hidkey

            if caps:
                write_report(chr(32)+NULL_CHAR + chr (hidkey) + NULL_CHAR*5)
            else:
                write_report(NULL_CHAR*2 + chr (hidkey) + NULL_CHAR*5)

            write_report(NULL_CHAR*8)
