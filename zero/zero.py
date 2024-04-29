import zmq
import sys
import logging
import socket as skt


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

while True:
    message = socket.recv()
    token = message.decode('utf-8')
    IP = skt.gethostbyname(skt.gethostname())
    print(IP)

    logging.info(f"Received request: {message}")
    logging.info(f"IP: {IP}")

    if check_token(token):
        print("Received request:", message)
        socket.send(b"World")
    else:
        socket.send(b"Error token")
