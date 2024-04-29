import codecs
import logging
import socket

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
    # Выводим информацию о клиенте
    # print("Подключение от клиента:", client_address)
    print(codecs.encode(client_address[0], 'utf-8').decode())
    # ip_address, port_number = client_address
    # print(f"Подключение от клиента: {ip_address}:{port_number}"
    # Проверяем IP адрес клиента
    # if client_address[0] == '77.120.144.152':  # Пример проверки IP адреса
    if client_address[0] == '46.211.229.139':  # Пример проверки IP адреса
        data = client_socket.recv(1024)
        if data:
            msg_client = data.decode()
            logging.info(f"IP: {msg_client}")

        client_socket.sendall(b"IP is correct")
    else:
        print("IP is failed")
        client_socket.sendall(b"IP is failed")
        client_socket.close()
        continue

    # Принимаем данные от клиента и отправляем ответ


    # Закрываем соединение с клиентом
    client_socket.close()
