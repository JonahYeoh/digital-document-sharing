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
    read_private_key.close()
    print(string)
    return string

def decrypt(dic, key):#解密
    private_key=RSA.import_key(key)
    cipherRSA = PKCS1_OAEP.new(private_key)
    # unpacking
    encSessionKey = base64.b16decode(dic["encSessionKey"].encode('ascii'))
    cipher_text = base64.b16decode(dic["ciphertext"].encode('ascii'))
    tag = base64.b16decode(dic["tag"].encode('ascii'))
    nonce = base64.b16decode(dic["nonce"].encode('ascii'))

    sessionKey = cipherRSA.decrypt(encSessionKey)

    cipherAES = AES.new(sessionKey, AES.MODE_EAX, nonce)
    
    plain_text = cipherAES.decrypt_and_verify(cipher_text, tag)
    return plain_text.decode("utf-8")

def encrypt(message, key): # 加密
    session_key = get_random_bytes(16)
    cipherAES = AES.new(session_key, AES.MODE_EAX)
    nonce = cipherAES.nonce
    byte_string = bytes(message, 'utf-8')
    ciphertext, tag = cipherAES.encrypt_and_digest(byte_string)

    b16_nonce = base64.b16encode(nonce)
    b16_ciphertext = base64.b16encode(ciphertext)
    b16_tag = base64.b16encode(tag)

    rsa_key = RSA.import_key(key)
    cipherRSA = PKCS1_OAEP.new(rsa_key)
    encSessionKey = cipherRSA.encrypt(session_key)
    b16_encSessionKey = base64.b16encode(encSessionKey)

    str16_nonce = b16_nonce.decode('ascii')
    str16_ciphertext = b16_ciphertext.decode('ascii')
    str16_tag = b16_tag.decode('ascii')
    str16_encSessionKey = b16_encSessionKey.decode('ascii')
    # packing
    secret = {"encSessionKey" : str16_encSessionKey,
            "tag" : str16_tag,
            "ciphertext" : str16_ciphertext,
            "nonce" : str16_nonce}
    cipher_text = json.dumps(secret)
    return cipher_text.encode()