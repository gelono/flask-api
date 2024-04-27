import zmq

# Открытый/закрытый ключи сервера
server_public_key = b'jA8U*z0y7M59cxCMtH)L[?ornj><R@MLe)V>T5FX'
server_secret_key = b'dPoKlIUK&xI9wH:+]E1mhv(GSna]i-EUyUs{$Q=4'


def check_token(token):
    with open('../storage/tokens.txt', 'r') as file:
        tokens = file.read().splitlines()
        return token in tokens


context = zmq.Context.instance()

# Создаем серверный сокет и настраиваем безопасность
server_socket = context.socket(zmq.REP)
server_socket.curve_secretkey = server_secret_key
server_socket.curve_publickey = server_public_key
server_socket.curve_server = True
server_socket.bind("tcp://*:5000")

while True:
    message = server_socket.recv()
    token = message.decode('utf-8')
    if check_token(token):
        print(f"Received request: {token}")
        server_socket.send(b"World")
    else:
        server_socket.send(b"Error token")
