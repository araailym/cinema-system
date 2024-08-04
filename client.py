import socket


client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(("localhost",9999))


message=client.recv(1024).decode()

while message:
    client.send(input(message).encode())
    message=client.recv(1024).decode()

# message=client.recv(1024).decode()
# client.send(input(message).encode())

# message=client.recv(1024).decode()
# client.send(input(message).encode())

# message=client.recv(1024).decode()
# client.send(input(message).encode())


print(client.recv(1024).decode())
