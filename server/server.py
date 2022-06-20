import socket, threading

from getpass import getpass
from mysql.connector import connect, Error

host = '127.0.0.1'
port = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))

server.listen()

def registration(login, password):
    # Подключаемся к бд, смотрим существует ли такой пользователь в системе, регистрируем, если нет
    return True

def auth(login,password):
    #Подключаемся к бд, смотрим, есть ли пользователь в бд, авторизуем, если есть
    return True

def init():
    #Инициализируем интерфейс пользователя, выводим список чатов и каналов,контекстное меню на создание новых
    return True



