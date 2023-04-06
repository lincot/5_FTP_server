import socket


class MySocket():
    def __init__(self, sock: socket.socket):
        self.sock = sock
        self.buffer = b''

    def sendall(self, data: bytes):
        self.sock.sendall('{:04}'.format(len(data)).encode() + data)

    def recv(self, bufsize: int = 1024) -> bytes:
        if not self.buffer:
            self.buffer = self.sock.recv(bufsize)
            if not self.buffer:
                return None
        msg_len = int(self.buffer[:4].decode())
        data = self.buffer[4:4 + msg_len]
        self.buffer = self.buffer[4 + msg_len:]
        return data

    def accept(self):
        (sock, addr) = self.sock.accept()
        return (MySocket(sock), addr)

    def bind(self, address):
        self.sock.bind(address)

    def listen(self):
        self.sock.listen()

    def getsockname(self):
        return self.sock.getsockname()

    def settimeout(self, value):
        self.sock.settimeout(value)

    def setblocking(self, flag):
        self.sock.setblocking(flag)

    def connect(self, address):
        self.sock.connect(address)


DEFAULT_PORT = 9090


def get_port() -> int:
    port = input(f'server port ({DEFAULT_PORT}): ')
    if not port:
        return DEFAULT_PORT
    else:
        return int(port)
