from fun import get_private_key, encrypt, decrypt
import socket, json
HOST, PORT = '127.0.0.1', 8876
HOST_2, PORT_2 ='127.0.0.1', 8886
# get my own private key
myPrivateKey = get_private_key("C:\\Users\\h702_1\.ssh\\id_rsa")
ssocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ssocket.bind((HOST, PORT))
ssocket.listen(5); print('server start at: %s:%s\nWaiting for connection...' % (HOST, PORT))
while True:
    conn, addr = ssocket.accept()
    # get caller id
    cipher_text = conn.recv(1024).decode()
    cipher_json = json.loads(cipher_text)
    caller_id = decrypt(cipher_json, myPrivateKey)
    print('connected by {} from {}'.format(caller_id, addr))
    # get caller public key
    db_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    db_socket.connect((HOST_2, PORT_2))
    db_socket.send(caller_id.encode())
    response = db_socket.recv(1024).decode()
    db_socket.close()
    response = response.split("$$$$$")
    dialerPublicKey = response[1]
    while response[0] == "200":
        try:
            cipher_text = conn.recv(1024).decode()
            cipher_json = json.loads(cipher_text)
            print("已收到:" + decrypt(cipher_json, myPrivateKey))
            if len(cipher_text) == 0:
                break
            plain_text = input("對答:")
            conn.send(encrypt(plain_text, dialerPublicKey))
        except:
            print("error")
            break
    conn.close()
    print('Disconnected with {} : {}'.format(caller_id, addr))