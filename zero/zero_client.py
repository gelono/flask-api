import zmq
import ssl


context = zmq.Context()
socket = context.socket(zmq.REQ)  # REQ (REQUEST) socket for sending requests

# Создаем SSL контекст
ssl_context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
ssl_context.load_verify_locations("vm5043127.43ssd.had.wf-crt.pem")  # Путь к сертификату сервера

socket = ssl_context.wrap_socket(socket, server_side=False)  # Оборачиваем сокет в SSL

socket.connect("tcp://vm5043127.43ssd.had.wf:5000")
# socket.connect("tcp://localhost:5000")

# socket.send(b"Hello")
socket.send(b"uaysdgfuqcyk13rkuahcvuy3115135")
message = socket.recv()
print(f"Received reply: {message.decode('utf-8')}")
