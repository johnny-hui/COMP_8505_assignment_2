import socket
import select
import sys

if __name__ == '__main__':
    # Create a socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific host and port
    server_address = ("localhost", 8080)
    server_socket.bind(server_address)

    # Listen for incoming connections
    server_socket.listen(5)

    # List of sockets to monitor for readability (includes the server socket)
    sockets_to_read = [server_socket, sys.stdin]

    # List to keep track of connected client sockets and their addresses
    connected_clients = {}

    print("[+] Server is listening on", server_address)

    while True:
        # Use select to monitor sockets for readability
        readable, _, _ = select.select(sockets_to_read, [], [])

        for sock in readable:
            if sock is server_socket:
                # This means there is a new incoming connection
                client_socket, client_address = server_socket.accept()
                print("New connection from:", client_address)
                sockets_to_read.append(client_socket)

                # Add the new client socket to the connected_clients dictionary
                connected_clients[client_socket] = client_address

            # Read from stdin file descriptor
            elif sock is sys.stdin:
                command = sys.stdin.readline().strip()

                if command == "connect":  # a) For Connecting to victim
                    target_ip = input("[+] Enter target IP address: ")
                    target_port = int(input("[+] Enter target port: "))
                    try:
                        # Create a new client socket and initiate the connection
                        target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        target_socket.connect((target_ip, target_port))
                        print("[+] Connected to", (target_ip, target_port))

                        # Add the new client socket to the connected_clients dictionary
                        connected_clients[target_socket] = (target_ip, target_port)
                        sockets_to_read.append(target_socket)
                    except Exception as e:
                        print("[+] Connection error:", str(e))

                if command == "send":  # For Sending things to a specific victim
                    target_socket = None
                    target_ip = input("[+] Enter target IP address: ")
                    target_port = int(input("[+] Enter target port: "))
                    msg = input(f"[+] Type what you want to send to {target_ip} on port {target_port}: ")

                    # Find a specific client socket to send data to (if multiple clients)
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
                        print("[+] Target client not found!")

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
