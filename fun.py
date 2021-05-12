import socket
from Crypto.PublicKey import RSA
from Crypto.Protocol.KDF import PBKDF2
import random
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import json

import base64


def get_private_key(route):
    read_private_key=open(route,"rb")
    
    string=read_private_key.read()
    print(string)
    read_private_key.close()
    return string

def decrypt(dic,string):#解密
    private_key=RSA.import_key(string)
    cipherRSA = PKCS1_OAEP.new(private_key)
    sessionKey = cipherRSA.decrypt(base64.b16decode(dic["encSessionKey"].encode('ascii')))
    
    cipherAES = AES.new(sessionKey, AES.MODE_EAX, base64.b16decode(dic["nonce"].encode('ascii')))
    data = cipherAES.decrypt_and_verify(base64.b16decode(dic["ciphertext"].encode('ascii')), base64.b16decode(dic["tag"].encode('ascii')))
    return data.decode("utf-8")
def encrypt(message,string):#加密
    #read_public_key = open("C:\\Users\\h702_1\.ssh\\id_rsa.pub", "rb").read()
    #print(string)
    public_key= RSA.import_key(string)
    cipherRSA = PKCS1_OAEP.new(public_key)

    key =get_random_bytes(16)
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
    
    secret={"encSessionKey":str16_encSessionKey,"tag":str16_tag,"ciphertext":str16_ciphertext,"nonce":str16_nonce}
    json_secret=json.dumps(secret)
    #print(json_secret)
    outdata = json_secret
    print(outdata)
    return outdata.encode()
