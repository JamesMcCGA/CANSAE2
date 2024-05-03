import socket 
import os

def send_file(socket, filename):
    try:
        with open(filename, 'rb') as f:
            while True:
                bytes_read = f.read(4096)  # Read the file in chunks,  in order to support very large files
                if not bytes_read:
                    break  # File sending is done
                try:
                    print(f"Sending {len(bytes_read)} bytes")
                    socket.sendall(bytes_read)
                except socket.error as e:
                    print(f"Socket error: {e}")
                    raise
    except FileNotFoundError:
        print("File not found error")
    except Exception as e:
        print(f"Error: {e}")

def recv_file(socket, filename):
    if os.path.exists(filename):
        print("Error: file already exists")
        return 
    try:
        with open(filename, 'wb') as f:
            while True:
                try:
                    data = socket.recv(4096)
                    if not data:
                        break  
                    f.write(data)  
                    print(f"Received {len(data)} bytes, writing to file.")  # Debugging
                except socket.error as e:
                    print(f"Socket error: {e}")
                    raise
    except Exception as e:
        print(f"Error: {e}")


def send_listing(socket):
    try:
        files = os.listdir('server_data')
        list_str = '\n'.join(files)
        try:
            socket.sendall(list_str.encode())
        except socket.error as e:
            print(f"Socket error: {e}")
            raise
    except Exception as e:
        print(f"Error: {e}")

def recv_listing(socket):
    try:
        try:
            data = socket.recv(4096)
            print("Directory listing received: ")
            print(data.decode())
        except socket.error as e:
            print(f"Socket error: {e}")
            raise
    except Exception as e:
        print(f"Error: {e}")



