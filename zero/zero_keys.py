import zmq

context = zmq.Context()
server_keypair, _ = zmq.curve_keypair()

print(f"Сервер: Закрытый ключ: {server_keypair}")
print(f"Сервер: Закрытый ключ: {_}")