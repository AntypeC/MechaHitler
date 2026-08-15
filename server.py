import socket

# https://www.digitalocean.com/community/tutorials/python-socket-programming-server-client

def server_program():
    host = '127.0.0.1'  # loopback address for local testing
    port = 5000  # initiate port no above 1024

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # IPv4 TCP socket
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # allow port reuse immediately after server shutdown
    server_socket.bind((host, port))  # bind host address and port together

    server_socket.listen(5)  # queue up to 5 connection requests
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        raw = conn.recv(1024)  # read up to 1024 bytes; larger messages require multiple recv() calls
        if not raw:
            break
        try:
            data = raw.decode('utf-8')
        except UnicodeDecodeError:
            print(f"Received non-UTF-8 data from {address}, skipping")
            continue
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.sendall(data.encode())  # send data to the client

    conn.close()  # close the connection
    server_socket.close()  # close the listening socket


if __name__ == '__main__':
    server_program()