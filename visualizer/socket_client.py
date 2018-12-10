import socket
import threading

HOST = '127.0.0.1'
PORT = 9998

class SocketClient():

    def __init__(self, callback):
        
        self.callback = callback
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((HOST, PORT))
        self.socket.settimeout(0.03)
        self.lock = threading.Lock()
        threading.Thread(target = self.listen).start()
        
    def send(self, string):
        
        self.socket.send(string)
        
    def listen(self):
        
        while True:
            
            try:
                
                data = self.socket.recv(1024)
                if data:
                    self.callback(data)
                        
            except socket.timeout:
                pass
