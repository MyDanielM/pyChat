import socket
import sqlite3
import os.path
import threading


def getActiveUsers(clientSocket, clientAddr):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT login,addr,port FROM logged_users')
    users = cur.fetchall()
    for user in users:
        if clientAddr[0] == user[1] and clientAddr[1] == user[2]:
            msg = f'{user[0]} (it\'s you)\n'
        else:
            msg = f'{user[0]}\n'
        clientSocket.send(msg.encode())


def logOutAll():
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM logged_users')


def addLoggedUser(name: str, addr: str, port: int):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM logged_users')
    users = cur.fetchall()
    new_id = len(users)
    new_user = (new_id + 1, name, addr, port)

    cur.execute("""
        SELECT COUNT(*)
        FROM logged_users
        WHERE login = ? OR port = ?
    """, (new_user[1], new_user[-1],))
    flag = cur.fetchone()[0]

    if flag:
        print(f'Error! User {name} with {addr}:{port} already logged!')
    else:
        cur.execute('INSERT INTO logged_users VALUES( ?, ?, ?, ?);', new_user)
        conn.commit()
        print(f'User {name} {addr}:{port} log in.')
    conn.close()


def addNewUser(name: str, password: str, addr: str, port: int):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    new_id = len(users)
    new_user = (new_id + 1, name, password, addr, port)

    cur.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE login = ? OR port = ?
    """, (new_user[1], new_user[-1],))
    flag = cur.fetchone()[0]
    if flag:
        print(f'Error! Someone try use same info as {name} while refister!')
    else:
        cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?);', new_user)
        conn.commit()
        print(f'Added new user {name} {addr}:{port}.')
    conn.close()
    return flag


def initDB():
    conn = sqlite3.connect('users.db')

    cur = conn.cursor()
    if os.path.exists('users.db'):
        print('Connecting to DB...')
        print('Connection success!')
        conn.close()
    else:
        cur.execute("""CREATE TABLE IF NOT EXISTS users(
        userid INT PRIMARY KEY,
        login TEXT,
        password TEXT,
        addr TEXT,
        port TEXT);
        """)
        conn.commit()

        cur.execute("""INSERT INTO users(userid, login, password, addr, port) 
        VALUES(?, ?, ?, ?, ?);""", (1, 'server', 'revres', '192.168.0.104', 65000))
        conn.commit()

        cur.execute("""CREATE TABLE IF NOT EXISTS logged_users(
                id INT PRIMARY KEY,
                login TEXT,
                addr TEXT,
                port TEXT);
                """)
        conn.commit()

        conn.close()


def getUser(name: str):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute('SELECT login, addr, port FROM users WHERE login = ?', (name,))
    user = cur.fetchone()
    conn.close()
    return user


def register(clientSocket, clientAddr):
    user = []
    clientSocket.send('Enter your login: '.encode())
    name = clientSocket.recv(1024).decode()
    clientSocket.send('Enter your password: '.encode())
    password = clientSocket.recv(1024).decode()
    user.append(name)
    user.append(password)
    user.append(clientAddr[0])
    user.append(clientAddr[1])

    err = addNewUser(user[0], user[1], user[2], user[3])
    if err:
        clientSocket.send('Error. This user already exist.'.encode())
    else:
        clientSocket.send('Success. Now you may log in.'.encode())


def login(clientSocket, clientAddr):
    user = []
    clientSocket.send('Enter your login: '.encode())
    name = clientSocket.recv(1024).decode()
    clientSocket.send('Enter your password: '.encode())
    password = clientSocket.recv(1024).decode()
    user.append(name)
    user.append(password)
    user.append(clientAddr[0])
    user.append(clientAddr[1])

    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM users WHERE login = ? AND port = ?', (user[0], user[-1]))
    flag = cur.fetchone()[0]
    if flag:
        addLoggedUser(user[0], user[2], user[3])
        msg = 'You are logged in. Welcome!'
        clientSocket.send(msg.encode())
    else:
        msg = 'We have no such user. You should register first...'
        print(f'{user[2]} tried to log in. Login or password incorrect.')
        clientSocket.send(msg.encode())


def mainThread(s):
    conn, addr = s.accept()
    print(f'Client {addr} connected!')
    msg = r'-r register, -l login, -u active users, -c <username> connect to user, -e exit.'
    conn.send(msg.encode())
    while True:
        rep = conn.recv(1024).decode()
        if rep == r'-r':
            thread = threading.Thread(target=register, args=(conn, addr,), daemon=True)
            thread.start()
            thread.join()
        if rep == r'-l':
            thread = threading.Thread(target=login, args=(conn, addr,), daemon=True)
            thread.start()
            thread.join()
        if rep == r'-u':
            thread = threading.Thread(target=getActiveUsers, args=(conn, addr), daemon=True)
            thread.start()
            thread.join()
        if rep == r'/e':
            logOutAll()
            s.close()


def listen():
    server = getUser('server')
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((server[1], server[2]))
    s.listen()
    print(f'Start listening for clients on {server[1]}:{server[2]}')
    main = threading.Thread(target=mainThread, args=(s,), daemon=True)
    main.start()
    main.join()


if __name__ == '__main__':
    try:
        initDB()
        listen()
    except Exception as e:
        print(f"Error! {e}")
