import socket, sys, select, thread
from multiprocessing.pool import ThreadPool

def handle_new_connection(conn):
    clients.add(conn)
    print "Added user"
    broadcast_message(conn, "User joined to chat. Greet him/her!", clients)

def listen_to_new_connections():
    while True:
        conn, addr = server_socket.accept()
        print "Connection recieved"
        handle_new_connection(conn)

def listen_to_client_messages():
    while True:
        if clients:
            try:
                read_clients, write_clients, error_clients = select.select(clients, clients, [])
                read_and_broadcast(read_clients, write_clients)
            except:
                print "Error!"

def read_and_broadcast(read_clients, write_clients):
    for client in read_clients:
        try:
            message = client.recv(4096)
            print "Message recieved"
        except: #windows throws exception when connection is closed
            message = ""
        if message:
            broadcast_message(client, message, write_clients)
        else:
            client.close()
            clients.remove(client)    

def broadcast_message(messaged_client, message, write_clients):
    for client in write_clients:
        if messaged_client != client:
            pool.apply_async(send_message, (client, message))

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

