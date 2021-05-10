import socket
from Crypto.PublicKey import RSA
from Crypto.Protocol.KDF import PBKDF2
import random
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import json
import base64

HOST = '127.0.0.1'
PORT = 8877
number="107316127"
HOST_2='192.168.0.238'
PORT_2=8886
s_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s.set_socket(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((HOST, PORT))
s.listen(5)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')

def decrypt(dic):

    privateKey = RSA.import_key(open("C:\\Users\\h702_1\.ssh\\id_rsa").read())

    cipherRSA = PKCS1_OAEP.new(privateKey)
    
    sessionKey = cipherRSA.decrypt(base64.b16decode(dic["encSessionKey"].encode('ascii')))
    
    cipherAES = AES.new(sessionKey, AES.MODE_EAX, base64.b16decode(dic["nonce"].encode('ascii')))
    data = cipherAES.decrypt_and_verify(base64.b16decode(dic["ciphertext"].encode('ascii')), base64.b16decode(dic["tag"].encode('ascii')))
    return data.decode("utf-8")
def encrypt(message):#加密
    read_public_key = open("C:\\Users\\h702_1\.ssh\\id_rsa2.pub", "rb").read()
    key =get_random_bytes(16)
    public_key= RSA.import_key(read_public_key)
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
    
    #db64 = str16_encSessionKey.encode('ascii')
    secret={"encSessionKey":str16_encSessionKey,"tag":str16_tag,"ciphertext":str16_ciphertext,"nonce":str16_nonce}
    json_secret=json.dumps(secret)
    #print(json_secret)
    outdata = json_secret
    return outdata.encode()
while True:
    conn, addr = s.accept()
    print('connected by ' + str(addr))

    while True:
        
        s_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_2.connect((HOST_2, PORT_2))
        s_2.send(number.encode())
        server = s_2.recv(1024).decode()
        status=server.split("$$$$$")
        s_2.close()
        if status[0]=="200":
            indata = conn.recv(1024)
            json_translate=json.loads(indata)
            print("已收到:"+decrypt(json_translate))
            if len(indata) == 0: # connection closed
                conn.close()
                print('client closed connection.')
                break
            #print('recv: ' + indata.decode())
            talk=input("對答:")

            #outdata = 'echo ' + indata.decode()

            conn.send(encrypt(talk))
            print("receive successful")
