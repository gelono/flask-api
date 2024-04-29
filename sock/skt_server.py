import codecs
import socket

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
    print('1')
    client_socket, client_address = server_socket.accept()
    print('2')
    # Выводим информацию о клиенте
    # print("Подключение от клиента:", client_address)
    print(codecs.encode(client_address[0], 'utf-8').decode())
    # ip_address, port_number = client_address
    # print(f"Подключение от клиента: {ip_address}:{port_number}")
    print('3')
    # Проверяем IP адрес клиента
    # if client_address[0] == '77.120.144.152':  # Пример проверки IP адреса
    if client_address[0] == '127.0.0.1':  # Пример проверки IP адреса
        print('4')
        print("IP is correct")
        client_socket.sendall(b"IP is correct")
    else:
        print('5')
        print("IP is failed")
        client_socket.sendall(b"IP is failed")
        client_socket.close()
        continue

    # Принимаем данные от клиента и отправляем ответ
    data = client_socket.recv(1024)
    print('6')
    if data:
        print('7')
        print("MSG from client:", data.decode())
        client_socket.sendall(b"Msg recived")
        print('8')

    # Закрываем соединение с клиентом
    client_socket.close()
    print('9')
