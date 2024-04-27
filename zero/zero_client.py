import zmq

# Открытый/закрытый ключи клиента
server_public_key = b'jA8U*z0y7M59cxCMtH)L[?ornj><R@MLe)V>T5FX'

client_public_key = b'y&u>jY?+%isnN7hhhoxkezFO^DpV*-kN{DO6z-qy'
client_secret_key = b'8lmlsf0MIf{Wte-P{<at34rBA:6XCegXv3KQ*A6m'

context = zmq.Context.instance()

# Создаем клиентский сокет и настраиваем безопасность
client_socket = context.socket(zmq.REQ)
client_socket.curve_secretkey = client_secret_key
client_socket.curve_publickey = client_public_key
client_socket.curve_serverkey = server_public_key
client_socket.connect("tcp://localhost:5000")

# Отправляем запрос на сервер
token = b"uaysdgfuqcyk13rkuahcvuy3115135"
client_socket.send(token)

# Получаем ответ от сервера
reply = client_socket.recv()
print(f"Received reply: {reply.decode('utf-8')}")
