import socket
from threading import *
import urllib.request, urllib.parse, urllib.error

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "127.0.0.1"
port = 4001
print (host)
print (port)
serversocket.bind((host, port))

class client(Thread):
    def __init__(self, socket, address):
        Thread.__init__(self, daemon=True)
        self.sock = socket
        self.addr = address
        self.start()

    def run(self):
        while 1:
            try:
                data = self.sock.recv(1024).decode()
                if not data or data == '':
                    continue
                web = urllib.request.urlopen(data)
                html = web.read()
                with open("temp.txt", 'wb+') as f:
                    f.write(html)
                    f.close()
                file = open("temp.txt", "rb")
                data = file.read()
                while data:
                    self.sock.send(data)
                    data = file.read(8192)
                    if not data:
                        self.sock.send(b'ENDOFFILE')
                        break
            except BrokenPipeError:
                print('connection closed')
                break

serversocket.listen(5)
print ('server started and listening')
while 1:
    clientsocket, address = serversocket.accept()
    print('Connected to', address)
    client(clientsocket, address)

