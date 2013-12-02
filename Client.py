import socket, sys, select
from multiprocessing.pool import ThreadPool


def listen_to_messages_from_user(server_socket):
    while True:
        try:
            message = sys.stdin.readline()
            server_socket.send(message)
        except:
            print "Server not responding. Quitting..."
            break;

def listen_to_new_messages():
    while True:        
        read_sockets, write_sockets, error_sockets = select.select([server_socket], [], [], 1)
        for s in read_sockets:
            try:
                message = s.recv(4096)
                sys.stdout.write(message)
            except:
                print "Server not responding. Quitting..."
                sys.exit(1)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 2023
server_socket.connect((host, port))

pool = ThreadPool(2)

pool.apply_async(listen_to_new_messages)
listen_to_messages_from_user(server_socket)