from fun import get_private_key, encrypt, decrypt
import socket
import json
HOST, PORT = '127.0.0.1', 8876
HOST_2, PORT_2 ='127.0.0.1', 8886
# get my own private key
myPrivateKey = get_private_key("C:\\Users\\h702_1\.ssh\\id_rsa")
#caller_id = "107316127" # suppose we do not know who will connect to us
# set up server
ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssocket.bind((HOST, PORT))
ssocket.listen(5); print('server start at: %s:%s\nWaiting for connection...' % (HOST, PORT))
while True:
    conn, addr = ssocket.accept()
    print('connected by ' + str(addr)) # insert capture dialer's id at line below
    # get caller's public key
    caller=conn.recv(1024).decode()
    json_translate = json.loads(caller)
    caller_id=decrypt(json_translate, myPrivateKey)

    db_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    db_socket.connect((HOST_2, PORT_2))
    db_socket.send(caller_id.encode())
    response = db_socket.recv(1024).decode()
    db_socket.close()
    response = response.split("$$$$$")
    dialerPublicKey = response[1]
    while response[0] == "200":
        try:
            indata = conn.recv(1024).decode()
            json_translate = json.loads(indata)
            print("已收到:" + decrypt(json_translate, myPrivateKey))
            if len(indata) == 0:
                break
            talk = input("對答:")
            conn.send(encrypt(talk, dialerPublicKey))
        except:
            print("error")
            break
    conn.close()
    print('Disconnected from {}'.format(addr))
