import queue
import socket
import constants
import importlib


def is_file_openable(file_path):
    try:
        with open(file_path, 'r') as file:
            pass
        return True
    except IOError as e:
        print(constants.FILE_CANNOT_OPEN_ERROR.format(file_path, e))
        return False


def is_importable(file_name: str):
    print(f"[+] Importing module {file_name}...")

    try:
        importlib.import_module(file_name)
        return True
    except ImportError as e:
        print(constants.FAILED_IMPORT_ERROR.format(file_name, e))
        return False
    except Exception as e:
        print(constants.FAILED_IMPORT_EXCEPTION_ERROR.format(file_name, e))
        return False


def watch_signal(client_socket: socket.socket, signal_queue: queue.Queue):
    while True:
        try:
            signal = client_socket.recv(100).decode()
            if signal == "STOP":
                print(constants.CLIENT_RESPONSE.format(signal))
                signal_queue.put(signal)
                return None
        except socket.timeout as e:
            print("[+] ERROR: Connection to client has timed out : {}".format(e))
            break
        except socket.error as e:
            print("[+] Socket error: {}".format(e))
            break
