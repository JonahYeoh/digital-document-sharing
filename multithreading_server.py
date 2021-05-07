import socket, threading
import os

LOCALHOST = "192.168.0.238"
PORT = 8886
db_path = 'db'
def search_public_key(id):
    fileName = (id+'.txt')
    dir = os.listdir(db_path)
    print(fileName, dir)
    if fileName in os.listdir(db_path):
        freader = open(os.path.join(db_path, fileName))
        public_key = freader.read()
        return '200$$$$$' + public_key
    else:
        return '404$$$$$id not found'

class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket, callbacks):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.execute = callbacks
        print ("New connection added: ", clientAddress)

    def run(self):
        print ("Connection from : ", clientAddress)
        #self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ''
        data = self.csocket.recv(2048)
        msg = data.decode()
        ret = self.execute(msg)
        print ("from client", msg)
        print('to client', ret)
        self.csocket.send(bytes(ret,'UTF-8'))
        self.csocket.close()
        print ("Client at ", clientAddress , " disconnected...")


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))
print("Server started")
print("Waiting for client request..")
while True:
    server.listen(5)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock, search_public_key)
    newthread.start()