import socket
import os
HOST = '192.168.0.238'  # Standard loopback interface address (localhost)
PORT = 8888        # Port to listen on (non-privileged ports are > 1023)
BUFLEN = 1024
ENCODING = 'utf-8'
K_LEN = 405

db_path = 'db'
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
seq = 0
while True:
    client_socket, address = server_socket.accept()
    client_socket.sendall('200:Hello {}, please enter (1) Registration, (2) Get Public Key Of Other User, (3) Close Connection'.format(seq).encode('utf-8'))
    data = client_socket.recv(BUFLEN)
    print(data)
    data_str = data.decode(ENCODING)
    if data_str == '1':
        msg = '200:Enter ID: '
        client_socket.sendall(msg.encode(ENCODING))
        uid = client_socket.recv(BUFLEN).decode(ENCODING)
        dst = '{}.txt'.format(uid)
        fail = 0
        while dst in os.listdir(db_path):
            print('Fail: ', fail)
            fail += 1
            if fail >= 10:
                warning_msg = '300:Exceed maximum trial'
                client_socket.sendall(warning_msg.encode(ENCODING))
                break
            redundant_error = '300:Same User ID exists'
            client_socket.sendall(redundant_error.encode(ENCODING))
            uid = client_socket.recv(BUFLEN).decode(ENCODING)
            dst = '{}.txt'.format(uid)
        if fail < 10:
            inst_msg = '200:Enter Public Key: '
            print(inst_msg)
            client_socket.sendall(inst_msg.encode(ENCODING))
            public_key = client_socket.recv(BUFLEN).decode(ENCODING)
            print(public_key)
            if len(public_key) == K_LEN:
                print('writing')
                new_user = open(os.path.join(db_path, dst), 'w')
                new_user.write(public_key)
                new_user.close()
            else:
                warning_msg = '500:Invalid Public Key: '
                client_socket.sendall(warning_msg.encode(ENCODING))
    elif data_str == '2':
        msg = '200:Enter ID: '
        client_socket.sendall(msg.encode(ENCODING))
        uid = client_socket.recv(BUFLEN).decode(ENCODING)
        dst = '{}.txt'.format(uid)
        if dst in os.listdir(db_path):
            user_file = open(os.path.join(db_path, dst), 'r')
            public_key = user_file.readline()
            user_file.close()
            msg = '{}:Public Key of {}={}'.format(777, uid, public_key)
            client_socket.sendall(msg.encode(ENCODING))
        else:
            warning_msg = '404:id not found'
            client_socket.sendall(warning_msg.encode(ENCODING))
    client_socket.close()
    seq += 1
print('Connection ended')
server.close()