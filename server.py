import socket
from gpt4all import GPT4All
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(script_dir, "Llama-3.2-3B-Instruct-abliterated.Q4_K_M.gguf")

model = GPT4All(model_path, allow_download=False) # downloads / loads a 4.66GB LLM

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
        user_entry = str(data)
        print("from connected user: " + user_entry)
        with model.chat_session():
            response = model.generate(user_entry, max_tokens=50)
            print(" -> "+ response)
        conn.sendall(response.encode())  # send data to the client

    conn.close()  # close the connection
    server_socket.close()  # close the listening socket


if __name__ == '__main__':
    server_program()

# modest, cute, grateful, nostalgic, feminine