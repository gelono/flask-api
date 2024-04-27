import zmq


context = zmq.Context()
socket = context.socket(zmq.REP)  # REP (REPLY) socket for responding to each request
socket.bind("tcp://*:5000")  # Listen on port 5000

while True:
    message = socket.recv()
    print(f"Received request: {message.decode('utf-8')}")
    socket.send(b"World")
