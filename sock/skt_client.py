import socket

# Создаем сокет
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Указываем IP и порт сервера
server_address = ('vm5043127.43ssd.had.wf', 5000)  # замените 'IP_сервера' на реальный IP адрес сервера
# server_address = ('localhost', 5000)  # замените 'IP_сервера' на реальный IP адрес сервера

try:
    # Подключаемся к серверу
    client_socket.connect(server_address)

    # Отправляем данные на сервер
    message = "uaysdgfuqcyk13rkuahcvuy3115135"

    client_socket.sendall(message.encode())

    # Ждем ответа от сервера
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print("Получено от сервера:", data.decode())
        except Exception as e:
            pass

finally:
    # Закрываем соединение
    client_socket.close()
