import os
import socket
import uuid
import subprocess
import platform
import sys

ip, port = '127.0.0.1', 4001

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((ip, port))
    flag = False
    print(str(sys.argv))
    website = sys.argv[1]
    s.send(website.encode())
    f = open("download.txt", "w+")
    print('website sent')
    while True:
        print('receiving data...')
        data = s.recv(8192).decode()
        if not data or data == '':
            continue
        if data.__contains__('ENDOFFILE'):
            data = data[:data.index('ENDOFFILE')]
            f.write(data)
            f.close()
            s.close()
            break
        f.write(data)



