import unittest, ChatClient, ChatServer, StringIO, time


class Test(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.host = "localhost"
        self.port = 5556
        self.server = ChatServer.ChatServer(self.host, self.port)
        self.server.start()

    @classmethod
    def tearDownClass(self):
        self.server.stop()
        
    def setUp(self):
        self.client1_stream = StringIO.StringIO()
        self.client2_stream = StringIO.StringIO()
        self.client3_stream = StringIO.StringIO()
        self.client1 = ChatClient.ChatClient(self.host, self.port, self.client1_stream, self.client1_stream)
        self.client2 = ChatClient.ChatClient(self.host, self.port, self.client2_stream, self.client2_stream)
        self.client3 = ChatClient.ChatClient(self.host, self.port, self.client3_stream, self.client3_stream)
    
    def tearDown(self):
        self.client1_stream.close()
        self.client2_stream.close()
        self.client3_stream.close()
        self.client1.disconnect()
        self.client2.disconnect()
        self.client3.disconnect()
        
    def WaitAbit(self):
        time.sleep(1)

    def test_clients_sends_messages__others_recieve(self):        
        message1 = "Hello Barak"       
        self.client1.send_message(message1)
                
        #wait for messages to arrive
        self.WaitAbit()
        
        self.assertEqual(self.client1.get_message_from_server(), self.server.greeting_message * 2)        
        self.assertEqual(self.client2.get_message_from_server(), self.server.greeting_message + message1)
        self.assertEqual(self.client3.get_message_from_server(), message1)
        
        message2 = "Hello Eliran"
        self.client3.send_message(message2)        
        
        #wait for messages to arrive
        self.WaitAbit()
            
        self.assertEqual(self.client1.get_message_from_server(), message2)        
        self.assertEqual(self.client2.get_message_from_server(), message2)
            
    
    def test_client_disconnects__server_successfully_removes_it(self):
        self.assertEqual(self.server.get_number_of_active_clients(), 3)
        self.client3.disconnect()
        self.WaitAbit()        
        self.assertEqual(self.server.get_number_of_active_clients(), 2)
    
    def test_client_disconnects__messages_are_still_delivered(self):
        message1 = "Hello client2"
        message2 = "Hello client3"
        self.client3.disconnect()
        self.WaitAbit()
        self.client1.send_message(message1)
        self.client2.send_message(message2)
        self.WaitAbit()
        self.assertEqual(self.client1.get_message_from_server(), self.server.greeting_message * 2 + message2)        
        self.assertEqual(self.client2.get_message_from_server(), self.server.greeting_message + message1)
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()