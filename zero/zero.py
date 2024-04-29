# import zmq
# import logging
#
# # Открытый/закрытый ключи сервера
# server_public_key = b'jA8U*z0y7M59cxCMtH)L[?ornj><R@MLe)V>T5FX'
# server_secret_key = b'dPoKlIUK&xI9wH:+]E1mhv(GSna]i-EUyUs{$Q=4'
#
# # Инициализация системы логирования
# logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')
#
# def check_token(token):
#     with open('../storage/tokens.txt', 'r') as file:
#         tokens = file.read().splitlines()
#         return token in tokens
#
#
# context = zmq.Context.instance()
#
# # Создаем серверный сокет и настраиваем безопасность
# server_socket = context.socket(zmq.REP)
# server_socket.curve_secretkey = server_secret_key
# server_socket.curve_publickey = server_public_key
# server_socket.curve_server = True
# server_socket.bind("tcp://*:5000")
#
# while True:
#     message = server_socket.recv()
#     token = message.decode('utf-8')
#
#     # Запись входящего сообщения в журнал
#     logging.info(f"Received request: {token}")
#
#     if check_token(token):
#         print(f"Received request: {token}")
#         server_socket.send(b"World")
#     else:
#         server_socket.send(b"Error token")
import zmq
import sys
import ssl
import logging
import socket


def check_token(token):
    with open('../storage/tokens.txt', 'r') as file:
        tokens = file.read().splitlines()
        return token in tokens


# # Инициализация системы логирования
logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

port = "5000"
if len(sys.argv) > 1:
    port = sys.argv[1]
    int(port)

# Создаем серверный сокет с типом "zmq.REP" и привязываем его к известному порту
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)

# Настройка TLS/SSL
# context_ssl = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
# context_ssl.load_cert_chain(certfile=r'C:\wacs\crt\vm5043127.43ssd.had.wf-crt.pem',
#                             keyfile=r'C:\wacs\crt\vm5043127.43ssd.had.wf-key.pem')

while True:
    message = socket.recv()

    # Получаем информацию о сокете
    client_address = socket.getsockopt_string(zmq.LAST_ENDPOINT)
    client_ip = client_address.split(":")[1]

    token = message.decode('utf-8')

    logging.info(f"Received request: {message}")
    logging.info(f"Received request: {client_ip}")

    if check_token(token):
        print("Received request:", message)
        socket.send(b"World")
    else:
        socket.send(b"Error token")
