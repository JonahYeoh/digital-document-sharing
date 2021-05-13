import socket
import json
from fun import encrypt, decrypt, get_private_key
HOST, PORT = '127.0.0.1', 8876
HOST_2, PORT_2='127.0.0.1', 8886
# get my own private key
myPrivateKey = get_private_key("C:\\Users\\h702_1\.ssh\\id_rsa2")
# get receiver's public key
db_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
db_socket.connect((HOST_2, PORT_2))
receiver_id = "107316126"#id_rsa2,id_rsa.pub
db_socket.send(receiver_id.encode())
response = db_socket.recv(1024).decode()
db_socket.close()
response=response.split("$$$$$")
receiverPublicKey = response[1]; # print(receiverPublicKey);
# connect to receiver
rsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rsocket.connect((HOST, PORT))
my_id="107316127"
rsocket.send(encrypt(my_id,receiverPublicKey))

while response[0] == "200":
    try:
        message = input("對答:")
        rsocket.send(encrypt(message,receiverPublicKey))
        indata = rsocket.recv(1024)
        json_translate = json.loads(indata)
        print("已收到:" + decrypt(json_translate, myPrivateKey))
        if len(indata) == 0:
            break
    except:
        print("error")
        break
rsocket.close()
print('Disconnected from ({}, {})'.format(HOST, PORT))
