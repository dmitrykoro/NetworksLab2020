import socket
import sys
from threading import Thread
from datetime import datetime
from colorama import init

init()

HOST = 'localhost'
PORT = 8080
BLOCK_SIZE = 1024



def main():
    
    def _init():
        global clientSocket
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((HOST, PORT))      
        Thread(target = _receive).start()
        Thread(target = _send).start()
        
             
        
    def _send():
        global clientSocket
        userName = input("Enter your username: ")
        
        while True:
            
            msg = f"\1[{userName}]:\1 {input()}".encode("utf-8")
            
            try:
                clientSocket.send(msg)
                
            except ConnectionResetError:
                handleException()
                
           
           
    def _receive():
        global clientSocket
        
        while True:
            try:

                data = clientSocket.recv(BLOCK_SIZE).decode("utf-8").strip("\1")
                
                if not data:
                    break
                   
                try:
                
                    message = data.split("\1")
                    header = (data.split("\1"))[0] + (data.split("\1"))[1]
                    data = (data.split("\1"))[2]
                    
                    print (header + data)
                    
                except IndexError:
                    print(data)
                
                
            except ConnectionResetError:
                handleException()
                
             
             
    def handleException():
        print("The server shutted down the connection")
        sys.exit(1)
        

    _init()
     
    

    
if __name__ == '__main__':
    main()
    