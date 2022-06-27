import socket

UPD_MAX_SIZE=65535

def listen(host: str = '127.0.0.1', port: int = 8080):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind((host, port))

    print(f'Слушаю по адресу: {host}:{port}')

    members = []
    while True:
        msg, addr = s.recvfrom(UPD_MAX_SIZE)

        if addr not in members:
            members.append(addr)

        if not msg:
            continue

        client_id = addr[1]
        msg_text = msg.decode('ascii')
        if msg_text == '__join':
            print(f'Клиент {client_id} присоединился!')
            continue

        message_template = '{}__{}'

        if msg_text == '__members':
            print(f'Клиент {client_id} запросил список пользователей')
            active_members = [f'client{m[1]}' for m in members if m != addr]
            members_msg = ';'.join(active_members)
            s.sendto(message_template.format('members', members_msg).encode('ascii'), addr)
            continue


if __name__ == '__main__':
    print('Сервер запущен...')
    try:
        listen()
    except Exception as e:
        print(f"Ошибка: {e}")
        print("Сервер завершил работу")
