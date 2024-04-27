import zmq


context = zmq.Context()
socket = context.socket(zmq.REQ)  # REQ (REQUEST) socket for sending requests
socket.connect("tcp://vm5043127.43ssd.had.wf:5000")

socket.send(b"Hello")
message = socket.recv()
print(f"Received reply: {message.decode('utf-8')}")
