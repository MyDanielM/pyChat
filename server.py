import socket
import sqlite3
import os.path


def addUser(login: str, password: str, addr: str, port: int):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    new_id = len(users)
    new_user = (new_id + 1, login, password, addr, port)

    cur.execute("""
        SELECT COUNT(*)
        FROM users
        WHERE login = ? OR port = ?
    """, (new_user[1], new_user[-1],))
    flag = cur.fetchone()[0]

    if flag:
        print(f'Error! User {login} with {addr}:{port} already exist!')
    else:
        cur.execute('INSERT INTO users VALUES(?, ?, ?, ?, ?);', new_user)
        conn.commit()
        print(f'Added new user {login} {addr}:{port}.')
    conn.close()

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
        VALUES('1', 'server', 'revres', '46.42.23.187', 8080);""")
        conn.commit()
        conn.close()

def getUser(login: str):
    conn = sqlite3.connect('users.db')
    cur = conn.cursor()

    cur.execute('SELECT login, addr, port FROM users WHERE login = ?', (login,))
    user = cur.fetchall()
    conn.close()
    return user

def listen():
    server = socket.socket()


if __name__ == '__main__':
    try:
        initDB()

    except Exception as e:
        print(f"Error! {e}")
