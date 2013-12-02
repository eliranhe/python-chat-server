import socket, sys, select, threading
import time
from threading import Thread
from multiprocessing.pool import ThreadPool


class ChatClient:
    def __init__(self, host, port, output_stream, input_stream):
        self.active = True
        self.output = output_stream
        self.input = input_stream
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.host = "localhost"
        self.port = 2023
        self.server_socket.connect((host, port))
        
        self.pool = ThreadPool(2)
    
    def start(self):   
        self.pool.apply_async(self.listen_to_new_messages)
        self.pool.apply_async(self.listen_to_messages_from_user)        

    def disconnect(self):
        if self.active:
            self.active = False
            self.server_socket.shutdown(socket.SHUT_RDWR)
            self.server_socket.close()

    def send_message(self, message):
        self.server_socket.send(message)

    def listen_to_messages_from_user(self):
        while self.active:
            try:
                message = self.input.readline()
                self.send_message(message)
            except:
                print "Server not responding. Quitting..."
                break;
    

    def get_message_from_server(self):
        return self.server_socket.recv(4096)

    def listen_to_new_messages(self):
        while self.active:        
            read_sockets, write_sockets, error_sockets = select.select([self.server_socket], [], [], 1)
            for s in read_sockets:
                try:
                    message = self.get_message_from_server()
                    self.output.write(message)
                except:
                    print "Server not responding. Quitting..."
                    sys.exit(1)
                    
if __name__ == '__main__':        
    chat_client = ChatClient("localhost", 2023, sys.stdout, sys.stdin)
    chat_client.start()
    
    while chat_client.active:
        time.sleep(1000)
