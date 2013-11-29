import socket, sys, select
from multiprocessing.pool import ThreadPool

def listen_to_new_connections():
    while True:
        conn, addr = server_socket.accept()
        clients.add(conn)
        # send_message(conn,"Welcome to my chat server!")
        # pool.apply_async(send_message, (conn, "Welcome to my chat server!"))
        print "Connection Recieved!"

def listen_to_client_messages():
    while True:
        if clients:
            read_clients, write_clients, error_client = select.select(clients, [], [], 1)       
            for client in read_clients:
                print client
                message = client.recv(4096)
                broadcast_message(client, message)
                

def broadcast_message(client, message):
    for active_client in clients:
        if active_client != client:
            pool.apply_async(send_message, (active_client, message))

def send_message(client, message):
    client.send(message)
    client.flush()

clients = set([])
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "localhost"
port = 2023
server_socket.bind((host, port))
server_socket.listen(10)

pool = ThreadPool(100)

pool.apply_async(listen_to_new_connections)
pool.apply_async(listen_to_client_messages)

sys.stdin.read(1)

