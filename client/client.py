import socket, threading

name = input('Enter your name: ')

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = input('Enter server addr: ')
port = int(input('Enter server port: '))
client.connect((host, port))

