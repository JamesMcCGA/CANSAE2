import socket
import sys
import os

from common_utilities import send_file, recv_file, recv_listing

# Hard-coded, absolute path to client data folder. If this is none, the program will use the client-data folder that already exists in the main folder.
client_data_dir = None


def main():
    if len(sys.argv) < 4:
        print("Usage: python client.py <hostname> <port> <command> [<filename>]")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    command = sys.argv[3]

    if len(sys.argv) > 4:
        filename = sys.argv[4]
    else:
        filename = None

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = (hostname, port)
    print(f"Connecting to {server_address[0]} port {server_address[1]}")
    sock.connect(server_address)

    try:
        command_string = f"{command} {filename}\n" if filename else f"{command}\n"        
        sock.sendall(command_string.encode('utf-8'))
        if command == "put" and filename:
            send_file(sock, filename)
            print("File uploaded successfully")
        elif command == "get" and filename:
            if client_data_dir == None:
                save_path = os.path.join('client_data', filename)
            else:
                save_path = client_data_dir
            recv_file(sock, save_path)
            print("File downloaded successfully")
        elif command == "list":
            recv_listing(sock)
        else:
            print("Invalid command or missing filename")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()