import socket
import threading
import base64

remote_ip   = "192.168.1.107"
remote_port = 3180

local_port = 9229

class ClientCon(threading.Thread):

    def __init__(self, client, server):
        threading.Thread.__init__(self)
        #self.daemon = True
        self._client = client
        self._server = server

    def run(self):
        while True:
            self._data = self._client.recv(8192)
            print " - - - - - Client -> Server - - - - - " + self._data
            if not self._data:
                break
            self._server.sendall(base64.b64encode(self._data))

class ServerCon(threading.Thread):

    def __init__(self, server, client):
        threading.Thread.__init__(self)
        #self.daemon = True
        self._server = server
        self._client = client

    def run(self):
        while True:
            self._data = self._server.recv(8192)
            print " - - - - - Server -> Client - - - - - " + self._data
            if not self._data:
                break
            self._client.send(base64.b64decode(self._data))

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wait for client to connect
clientSock.bind(("localhost", local_port))
clientSock.listen(1)
client, addr = clientSock.accept()

# Connect to server
serverSock.connect((remote_ip, remote_port))

cc = ClientCon(client, serverSock)
sc = ServerCon(serverSock, client)
cc.start()
sc.start()
