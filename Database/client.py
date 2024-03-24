import socket
import os

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(("localhost", 5001))
print("connected")

file = open("/Users/shaivigandhi/Desktop/OBC-AI/DSS-MANTIS-OBC-AI/Database/OBC_test_img.jpg", "rb")

data = file.read()

client.send(len(data).to_bytes(4, 'big'))
print("sent file size")

client.sendall(data)
print('sent the image')

