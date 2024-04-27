import zmq
import ssl


def check_token(token):
    with open('../storage/tokens.txt', 'r') as file:
        tokens = file.read().splitlines()
        return token in tokens


context = zmq.Context()
socket = context.socket(zmq.REP)  # REP (REPLY) socket for responding to each request

# Создаем SSL контекст
ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
ssl_context.load_cert_chain(
    certfile=r'C:\wacs\crt\vm5043127.43ssd.had.wf-crt.pem',
    keyfile=r'C:\wacs\crt\vm5043127.43ssd.had.wf-key.pem')  # Путь к сертификату и ключу сервера

socket = ssl_context.wrap_socket(socket, server_side=True)  # Оборачиваем сокет в SSL

socket.bind("tcp://*:5000")  # Listen on port 5000

while True:
    message = socket.recv()
    token = message.decode('utf-8')
    if check_token(token):
        print(f"Received request: {token}")
        socket.send(b"World")
    else:
        socket.send(b"Error token")
