import fun
import socket
import json
HOST = '127.0.0.1'
PORT = 8876
number="107316127"#id_rsa,id_rsa_pub
HOST_2='127.0.0.1'
PORT_2=8886
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

print('server start at: %s:%s' % (HOST, PORT))
print('wait for connection...')
while True:
    conn, addr = s.accept()
    print('connected by ' + str(addr))
    while True:
        try:
            s_2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s_2.connect((HOST_2, PORT_2))
            s_2.send(number.encode())
            server = s_2.recv(1024).decode()
            status=server.split("$$$$$")
            s_2.close()
            if status[0]=="200":
                indata = conn.recv(1024)
                json_translate=json.loads(indata)
                print("已收到:"+fun.decrypt(json_translate,fun.get_private_key("C:\\Users\\h702_1\.ssh\\id_rsa")))
                if len(indata) == 0: # connection closed
                    conn.close()
                    print('client closed connection.')
                    break
                talk=input("對答:")
                conn.send(fun.encrypt(talk,status[1]))
                print("receive successful")
            else:
                print("no found")
        except:
            print("error")
