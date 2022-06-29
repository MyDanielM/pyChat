import socket
import threading


def listen(s):
    while True:
        msg = s.recv(1024).decode()
        if len(msg)>0:
            print(msg)



def connect():
    s = socket.socket()
    s.connect(('192.168.0.104', 65000))

    thread = threading.Thread(target=listen, args=(s,), daemon=True)
    thread.start()

    while True:
        msg = input()
        s.send(msg.encode())




if __name__ == '__main__':
    print('Welcome to chat!')
    try:
        connect()
    except Exception as e:
        print(f'Error! {e}')