import fun
import socket
import json

HOST = '127.0.0.1'
PORT = 8876
HOST_2='127.0.0.1'
PORT_2=8886
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
number="107316126"#id_rsa2,id_rsa.pub

while True:
    try:
        s_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s_2.connect((HOST_2, PORT_2))
        s_2.send(number.encode())
        server = s_2.recv(1024).decode()
        status=server.split("$$$$$")
        s_2.close()
        if status[0]=="200":
            print(status[1])
            message=input("對答:")
            s.send(fun.encrypt(message,status[1]))
            indata = s.recv(1024)
            json_translate=json.loads(indata)
            print("已收到:"+fun.decrypt(json_translate,fun.get_private_key("C:\\Users\\h702_1\.ssh\\id_rsa2")))
            
            if len(indata) == 0: # connection closed
                s.close()
                print('server closed connection.')
                break
        else:
            print("no found")
    except:
        print("error")
    
    #print('recv: ' + indata.decode())
