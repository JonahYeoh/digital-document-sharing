import socket
from Crypto.PublicKey import RSA
from Crypto.Protocol.KDF import PBKDF2
import random
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import json

import base64

# 產生 256 位元隨機金鑰（32 位元組 = 256 位元）



read_public_key = open("C:\\Users\\h702_1\.ssh\\id_rsa.pub", "rb").read()


HOST = '127.0.0.1'
PORT = 8877
HOST_2='192.168.0.238'
PORT_2=8886
s_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s_2.connect((HOST_2, PORT_2))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
number="107316126"
def decreat(dic):
    privateKey = RSA.import_key(open("C:\\Users\\h702_1\.ssh\\id_rsa2").read())

    cipherRSA = PKCS1_OAEP.new(privateKey)
    
    sessionKey = cipherRSA.decrypt(base64.b16decode(dic["encSessionKey"].encode('ascii')))
    
    cipherAES = AES.new(sessionKey, AES.MODE_EAX, base64.b16decode(dic["nonce"].encode('ascii')))
    data = cipherAES.decrypt_and_verify(base64.b16decode(dic["ciphertext"].encode('ascii')), base64.b16decode(dic["tag"].encode('ascii')))
    return data.decode("utf-8")
while True:
    s_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_2.connect((HOST_2, PORT_2))
    s_2.send(number.encode())
    server = s_2.recv(1024).decode()
    status=server.split("$$$$$")
    s_2.close()
    if status[0]=="200":
        message=input("對答:")
        key =get_random_bytes(16)
        public_key= RSA.import_key(status[1])
        cipherRSA = PKCS1_OAEP.new(public_key)
        encSessionKey = cipherRSA.encrypt(key)

        cipherAES = AES.new(key, AES.MODE_EAX)
        nonce = cipherAES.nonce
        b = bytes(message, 'utf-8')


        ciphertext, tag = cipherAES.encrypt_and_digest(b)

        b16_nonce=base64.b16encode(nonce)
        b16_encSessionKey = base64.b16encode(encSessionKey)
        b16_tag=base64.b16encode(tag)
        b16_ciphertext=base64.b16encode(ciphertext)

        str16_nonce= b16_nonce.decode('ascii')
        str16_encSessionKey = b16_encSessionKey.decode('ascii')
        str16_tag=b16_tag.decode('ascii')
        str16_ciphertext=b16_ciphertext.decode('ascii')

        db64 = str16_encSessionKey.encode('ascii')
        #print(db64)
        secret={"encSessionKey":str16_encSessionKey,"tag":str16_tag,"ciphertext":str16_ciphertext,"nonce":str16_nonce}
        json_secret=json.dumps(secret)
        #print(json_secret)
        outdata = json_secret
    
    
        s.send(outdata.encode())

        indata = s.recv(1024)
        json_translate=json.loads(indata)
        print("已收到:"+decreat(json_translate))
        if len(indata) == 0: # connection closed
            s.close()
            print('server closed connection.')
            break
    #print('recv: ' + indata.decode())
