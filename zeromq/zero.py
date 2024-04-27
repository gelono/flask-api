import zmq


def check_token(token):
    with open('../storage/tokens.txt', 'r') as file:
        tokens = file.read().splitlines()
        return token in tokens


context = zmq.Context()
socket = context.socket(zmq.REP)  # REP (REPLY) socket for responding to each request
socket.bind("tcp://*:5000")  # Listen on port 5000

while True:
    message = socket.recv()
    token = message.decode('utf-8')
    if check_token(token):
        print(f"Received request: {token}")
        socket.send(b"World")
    else:
        socket.send(b"Error token")
