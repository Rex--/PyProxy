import socket
import threading

local_port = 22

remote_port = 3180

class ClientCon(threading.Thread):

    def __init__(self, client, service):
        threading.Thread.__init__(self)
        self._client = client
        self._service = service

    def run(self):
        while True:
            self._data = self._client.recv(4096)
            if not self._data:
                break
            self._service.sendall(self._data)

class ServiceCon(threading.Thread):

    def __init__(self, service, client):
        threading.Thread.__init__(self)
        self._service = service
        self._client = client

    def run(self):
        while True:
            self._data = self._service.recv(4096)
            if not self._data:
                break
            self._client.sendall(self._data)

clientSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serviceSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Wait until client connects to connect to the service
clientSock.bind(("", remote_port))
clientSock.listen(1)
client, addr = clientSock.accept()

# Connect to service
serviceSock.connect(("localhost", local_port))

cc = ClientCon(client, serviceSock)
sc = ServiceCon(serviceSock, client)

cc.start()
sc.start()
