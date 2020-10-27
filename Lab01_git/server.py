import socket
from threading import Thread
from datetime import datetime


HOST = 'localhost'
PORT = 8080
BLOCK_SIZE = 1024

connectedUsers = []


def main():
    
    def _init():
        global serverSocket
        serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serverSocket.bind((HOST, PORT))
        serverSocket.listen(5)
        print('waiting for connection...')
        Thread(target = _connect).start()
        
        
        
    def _connect():
        global conn
        while True:
            conn, address = serverSocket.accept()
            print ('connected:', address)
            connectedUsers.append(conn) 
            Thread(target = _send, args = (conn,)).start()
    
    
    
    def _send(conn):
        try:
            while True:
                data = conn.recv(BLOCK_SIZE).decode("utf-8")
                
                if not data:
                    break
                   
                now = datetime.now()
                currentTime = now.strftime("%H:%M:%S")
            
                timestamp = f"<{currentTime}> "
                print(timestamp)
                print(data[0])
                
                
                for receiver in connectedUsers:
                    try:
                        if (data[0] == "\1"):
                            receiver.send((timestamp + data).encode("utf-8"))
                        else:
                            receiver.send((data).encode("utf-8"))
                            
                    except ConnectionResetError:
                        print("This user disconnected")
                    
        except ConnectionResetError:
            pass
                 

        
    Thread(target = _init).start()
    
   
        
if __name__ == '__main__':
    main()

        
    
