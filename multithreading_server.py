import socket, threading, os
HOST, PORT = "192.168.0.238", 8886
db_path = 'db'
def search_public_key(uid):
    fileName = uid + '.txt'
    if fileName in os.listdir(db_path):
        with open(os.path.join(db_path, fileName), "r") as freader:
            public_key = freader.read()
        return '200$$$$$' + public_key
    return '404$$$$$uid not found'

class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket, callbacks):
        threading.Thread.__init__(self)
        self.csocket, self.clientAddress = clientsocket, clientAddress
        self.execute = callbacks
        print ("New connection added: ", clientAddress)

    def run(self):
        uid = self.csocket.recv(2048).decode('utf-8')
        outdata = self.execute(uid)
        self.csocket.send(bytes(outdata,'utf-8'))
        self.csocket.close()
        print ("Client at ", self.clientAddress , " disconnected...")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
while True:
    print("Waiting for client request..")
    server.listen(5)
    clientsock, clientAddress = server.accept()
    newthread = ClientThread(clientAddress, clientsock, search_public_key)
    newthread.start()