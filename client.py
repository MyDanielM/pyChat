import socket
import random
import threading

UPD_MAX_SIZE = 65535

COMMANDS = (
    '/members',
    '/connect',
    '/exit',
    '/help',
)

HELP_TEXT = """
/members - выводит пользователей
/connect <client> - подключает к собеседнику
/exit - отключает от собеседника
"""


def listen(s: socket.socket, host: str, port: int):
    while True:
        msg, addr = s.recvfrom(UPD_MAX_SIZE)
        msg_port = addr[-1]
        msg = msg.decode('ascii')
        allowed_ports = threading.current_thread().allowed_ports
        if msg_port not in allowed_ports:
            continue

        if not msg:
            continue

        if '__' in msg:
            command, content = msg.split('__')
            if command == 'members':
                for n, member in enumerate(content.split(';'), start=1):
                    print('\r\r' + f'{n}) {member}' + '\n' + 'сообщение: ', end='')
            else:
                peer_name = f'client{msg_port}'
                print('\r\r' + f'{peer_name}: ' + msg + '\n' + f'сообщение: ', end='')


def start_listen(target, socket, host, port):
    th = threading.Thread(target=target, args=(socket, host, port), daemon=True)
    th.start()
    return th


def connect(host='127.0.0.1', port=8080):
    own_port = random.randint(9000, 10000)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, own_port))

    listen_thread = start_listen(listen, s, host, port)
    allowed_ports = [port]
    listen_thread.allowed_ports = allowed_ports
    sendto = (host, port)

    s.sendto('__join'.encode('ascii'), sendto)

    while True:
        msg = input('Сообщение: ')

        command = msg.split(' ')[0]
        if command in COMMANDS:
            if msg == '/members':
                s.sendto('__members'.encode('ascii'), sendto)
            if msg == '/exit':
                peer_port = sendto[-1]
                allowed_ports.remove(peer_port)
                sendto = (host, port)
                print(f'Ты отключился от {peer_port}...')
            if msg.startswith('/connect'):
                peer = msg.split(' ')[-1]
                peer_port = int(peer.replace('client', ''))
                allowed_ports.append(peer_port)
                sendto = (host, peer_port)
                print(f'Ты подключился к {peer_port}!')

            if msg == '/help':
                print(HELP_TEXT)

        else:
            s.sendto(msg.encode('ascii'), sendto)


if __name__ == '__main__':
    print('Добро пожаловать в pyChat')
    connect()
