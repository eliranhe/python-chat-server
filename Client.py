import socket, sys, select
from multiprocessing.pool import ThreadPool

def listen_to_new_messages():
    while True:        
        read_sockets, write_sockets, error_sockets = select.select([server_socket], [], [], 1)
        for s in read_sockets:
            message = s.recv(4096)
            sys.stdout.write(message)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 2023
server_socket.connect((host, port))

pool = ThreadPool(2)

pool.apply_async(listen_to_new_messages)

while True:
    message = sys.stdin.readline()
    server_socket.send(message)