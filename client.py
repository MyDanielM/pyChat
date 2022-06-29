import socket

def connect():
    sock = socket.socket()
    sock.connect(('192.168.0.104', 65000))
    login = input('Enter you name: ')
    password = input('Enter password: ')
    user = []
    user.append(login)
    user.append(password)
    sock.send(user.encode())

    sock.close()

if __name__ == '__main__':
    print('Welcome to chat!')
    try:
        connect()
    except Exception as e:
        print(f'Error! {e}')