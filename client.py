
import socket

HOST = '192.168.0.238'  # Standard loopback interface address (localhost)
PORT = 8888        # Port to listen on (non-privileged ports are > 1023)
BUFLEN = 1024
ENCODING = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((HOST, PORT))
data = server.recv(BUFLEN)
data_str = data.decode(ENCODING)
print(data_str)
while len(data_str) != 0:
    print(data)
    request = input('Enter command:\t')
    server.sendall(request.encode(ENCODING))
    data = server.recv(BUFLEN)
    data_str = data.decode(ENCODING)


server.close()
