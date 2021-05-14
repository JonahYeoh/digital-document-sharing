from fun import encrypt, decrypt, get_private_key
import socket, json
HOST, PORT = '127.0.0.1', 8876 # ip and port of receiver
HOST_2, PORT_2 = '127.0.0.1', 8886
MYID = "107316127"
# get my own private key
myPrivateKey = get_private_key("C:\\Users\\h702_1\.ssh\\id_rsa2")
# get receiver's public key
db_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
db_socket.connect((HOST_2, PORT_2))
receiver_id = "107316126" # exchangeable
db_socket.send(receiver_id.encode())
response = db_socket.recv(1024).decode()
db_socket.close()
response = response.split("$$$$$")
receiverPublicKey = response[1]; # print(receiverPublicKey);
# connect to receiver
rsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rsocket.connect((HOST, PORT))
# ensure my id is only visible by the receiver
rsocket.send(encrypt(MYID, receiverPublicKey))
while response[0] == "200":
    try:
        plain_text = input("對答:")
        rsocket.send(encrypt(plain_text,receiverPublicKey))
        cipher_text = rsocket.recv(1024)
        cipher_json = json.loads(cipher_text)
        print("已收到:" + decrypt(cipher_json, myPrivateKey))
        if len(cipher_text) == 0:
            break
    except:
        print("error")
        break
rsocket.close()
print('Disconnected from {} : ({}, {})'.format(receiver_id, HOST, PORT))