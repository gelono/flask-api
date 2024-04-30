import logging
import socket

from functional import Web3WalletManager
from tools import check_ip, check_token

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

obj = Web3WalletManager("options.json")
commands = {
    1: obj.get_usdc_balance,
    2: obj.get_hyperliquid_user_state,
    3: obj.send_usdc_to_another_wallet,
    4: obj.send_usdc_to_hl,
    5: obj.hl_withdraw_test,
}

while True:
    client_socket, client_address = server_socket.accept()
    logging.info(f"IP: {client_address[0]}")

    if check_ip(client_address[0]):
        client_socket.sendall(b"IP is correct")

        data = client_socket.recv(1024)
        if data:
            try:
                message = eval(data.decode())  # Преобразовываем данные в словарь
                token = message.get("token")  # Извлекаем токен из словаря
                logging.info(f"token: {token}")
                print(token)
                if check_token(token):
                    client_socket.sendall(b"token is correct")
                    command = message.get("command")
                    amount = message.get("amount")
                    recipient = message.get("recipient")
                    commands[command]()

                else:
                    client_socket.sendall(b"token is incorrect")
            except Exception as e:
                logging.error(f"Error: {e}")
                client_socket.sendall(b"Invalid message format")
        else:
            client_socket.sendall(b"No token received")

    else:
        client_socket.sendall(b"IP is failed")

    client_socket.close()
