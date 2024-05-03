import socket
import os 
import sys

from common_utilities import *

def handle_client_connection(client_socket):
    try:
        request = client_socket.recv(1024).decode('utf-8').split('\n')[0].strip()
        parts = request.split() 
        command = parts[0]  
        args = parts[1:] if len(parts) > 1 else []

        print(f"Command: '{command}', Arguments: {args}")

        if command == "put" and args:
            filename = os.path.join('server_data', args[0])
            recv_file(client_socket, filename)
        elif command == "get" and args:
            filename = os.path.join('server_data', args[0])
            send_file(client_socket, filename)
        elif command == "list":
            send_listing(client_socket)
        else:
            print("Invalid command or arguments")

    except Exception as e:
        print(f"Error handling client {client_socket.getpeername()}: {e}")
    finally:
        client_socket.close()                

def start_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_address = ('', port)
    server_socket.bind(server_address)

    hostname = socket.gethostname()
    IPAddr = socket.gethostbyname(hostname)
    
    server_socket.listen(5)
    print(f"Server up and running on IP {IPAddr} port {port}")
    print("Waiting for a connection...")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")

        handle_client_connection(client_socket)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)
    
    port_number = int(sys.argv[1])
    start_server(port_number)