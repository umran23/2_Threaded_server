import socket 
from time import sleep

sock=socket.socket()
sock.setblocking(1)
sock.connect(('127.0.0.1',3000))



#message input()

msg= "HI!"

sock=sock.recv(1024)

sock.colse()
print(data.decode())
