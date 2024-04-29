import codecs
import logging
import socket


def check_token(token):
    with open('../storage/tokens.txt', 'r') as file:
        tokens = file.read().splitlines()
        return token in tokens


logging.basicConfig(filename='server.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Создаем сокет
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Указываем IP и порт для прослушивания
server_address = ('', 5000)  # пустая строка означает прослушивание всех доступных интерфейсов

# Привязываем сокет к заданному адресу и порту
server_socket.bind(server_address)

# Начинаем прослушивание входящих соединений
server_socket.listen(1)

print("server start...")

while True:
    # Принимаем входящее соединение
    client_socket, client_address = server_socket.accept()

    logging.info(f"IP: {client_address[0]}")
    if client_address[0] == '46.211.226.229':  # Пример проверки IP адреса
        data = client_socket.recv(1024)
        if data:
            token = data.decode()
            logging.info(f"token: {token}")
            if check_token(token):
                client_socket.sendall(b"token is correct")

        client_socket.sendall(b"IP is correct")

    else:
        print("IP is failed")
        client_socket.sendall(b"IP is failed")
        client_socket.close()
        continue

    # Закрываем соединение с клиентом
    client_socket.close()
