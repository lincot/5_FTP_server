from helpers import get_port, MySocket
from threading import Thread
from pathlib import Path
from time import sleep
import socket

DEFAULT_HOST = '127.0.0.1'


def get_host():
    host = input(f'server host ({DEFAULT_HOST}): ')
    if not host:
        return DEFAULT_HOST
    else:
        return host


def receive_loop(sock, outputs):
    while True:
        data = sock.recv()
        if data is None:
            return
        outputs.append(data)
        print(data.decode(), end='', flush=True)


def main():
    host = get_host()
    port = get_port()
    sock = MySocket(socket.socket())
    sock.setblocking(True)
    sock.connect((host, port))
    print(f'connected to {host}:{port}')
    outputs = []
    t = Thread(target=receive_loop, args=[sock, outputs])
    t.start()
    while t.is_alive():
        input_ = input()
        if input_.startswith('cpfrom'):
            input_ = input_[len('cpfrom '):]
            [src, dst] = input_.split(' ')
            src = Path(src).expanduser().resolve()
            with open(src, 'rb') as f:
                sock.sendall(b'wrfile ' + dst.encode() + b'\n' + f.read())
        elif input_.startswith('cpto'):
            input_ = input_[len('cpto '):]
            [src, dst] = input_.split(' ')
            dst = Path(dst).expanduser().resolve()
            len_before = len(outputs)
            sock.sendall(b'shfile ' + src.encode())
            while len(outputs) == len_before:
                sleep(0.01)
            with open(dst, 'wb') as f:
                f.write(outputs[-2][:-1])
        else:
            sock.sendall(input_.encode())


if __name__ == '__main__':
    main()
