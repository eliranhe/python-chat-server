import socket, sys, select, thread
from multiprocessing.pool import ThreadPool


class ChatServer:
    def __init__(self, host, port):
        self.active = True
        self.clients = set([])
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = host
        self.port = port
        self.server_socket.bind((host, port))
        self.server_socket.listen(10)
        
        self.pool = ThreadPool(100)
        self.greeting_message = "User joined to chat. Greet him/her!\r\n"
    
    def start(self):    
        self.pool.apply_async(self.listen_to_new_connections)
        self.pool.apply_async(self.listen_to_client_messages) 
        
    def stop(self):
        if self.active:
            self.active = False
            try:
                self.server_socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.server_socket.close()
        
    def handle_new_connection(self, conn):
        self.clients.add(conn)
        print "Added user"
        self.broadcast_message(conn, self.greeting_message, self.clients)

    def listen_to_new_connections(self):
        print "Listening"
        while self.active:
            conn, addr = self.server_socket.accept()
            print "Connection recieved"
            self.handle_new_connection(conn)
    
    def get_number_of_active_clients(self):
        return len(self.clients)
                
    def listen_to_client_messages(self):
        while self.active:
            if self.clients:
                try:
                    read_clients, write_clients, error_clients = select.select(self.clients, self.clients, [])
                    self.read_and_broadcast(read_clients, write_clients)
                except:
                    print "Error!"
    
    def read_and_broadcast(self, read_clients, write_clients):
        for client in read_clients:
            try:
                message = client.recv(4096)
                print "Message recieved"
            except:  # windows throws exception when connection is closed
                message = ""
            if message:
                self.broadcast_message(client, message, write_clients)
            else:
                client.close()
                self.clients.remove(client)
                print "User removed"    
    
    def broadcast_message(self, messaged_client, message, write_clients):
        for client in write_clients:
            if messaged_client != client:
                self.pool.apply_async(self.send_message, (client, message))
    
    def send_message(self, client, message):
        client.send(message)
        client.flush()
        
if __name__ == '__main__':
    if len(sys.argv) > 1:
        host = sys.argv[1]
    else:
        host = "localhost"
    
    if len(sys.argv) > 2:
        port = int(sys.argv[2])
    else:
        port = 2023 
          
    chat_server = ChatServer(host, port)
    print "Starting the server"
    chat_server.start()
    
    sys.stdin.read(1)
