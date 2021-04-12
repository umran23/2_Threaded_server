import socket
from threading import Thread


class Server:

    addr = ''
    port = 3030
    connections = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.logging('Socket has created')
        self.port, self.addr = self.ask_for_port_addr()
        self.bind()
        self.logging(f'Socket binded to port {self.port}')
        self.sock.listen(self.connections)
        self.logging(f'Socket is listening {self.connections} connections')
        self.main()

    @staticmethod
    def logging(data):
        with open("log_server.txt", "a") as f:
            f.write(f'{data}\n')

    def cleaning(self):
        with open("log_server.txt", "a") as f:
            f.write(f'\n{self.addr}, {self.port}')

    def main(self):
        try:
            while 1:
                conn, addr = self.sock.accept()
                self.logging(f'Client {addr} was connected')
                Thread(target=self.for_client, args=(conn,)).start()
        finally:
            self.logging('Server is closing')
            self.sock.close()

    def send(self, conn, message):
        assert len(message) <= 1024
        conn.send(f'{message}'.encode())
        self.logging(f'Sending this message {message}')

    def recv(self, conn):
        data = conn.recv(1024).decode()
        self.logging(f'Receiving a message => {data}')
        return data

    @staticmethod
    def for_port(port):
        try:
            if 1023 < int(port) < 65536:
                return True
            else:
                return False
        except ValueError:
            return False

    @staticmethod
    def for_ip(ip):
        try:
            sum = 0
            if ip == 'localhost':
                return True
            parts = ip.split(".", 4)
            if len(parts) == 4:
                for part in parts:
                    part = int(part)
                    if -1 < part < 256:
                        sum += 1
            else:
                return False
            if sum != 4:
                return False
        except ValueError:
            return False

    def ask_for_port_addr(self):
        user_port = input("Enter Port:")
        if self.for_port(user_port) is False:
            print(f'Wrong input, Port by Default is : -  {self.port}')
            user_port = str(self.port)

        user_ip = input("Enter IP Address:")
        if self.for_ip(user_ip) is False:
            print(f'Wrong Input, IP Address by Default is : -  {self.addr}')
            user_ip = self.addr
        return int(user_port), user_ip

    def bind(self):
        try:
            self.sock.bind((self.addr, self.port))
        except OSError:
            self.sock.bind((self.addr, 0))
            self.port = self.sock.getsockname()[1]
            print(f'New PORT is {self.port}')

    def for_client(self, conn):
        self.logging(f'Client {self.addr} was connected')
        while 1:
            data = self.recv(conn)
            if not data:
                self.logging(f'Client {self.addr} was disconnected\n')
                break
            if data == 'exit':
                self.logging('Сonnection is closing\n')
                break
            self.logging(f'Received message:{data}')
            self.logging(f'Sending message: {data}')
            self.send(conn, data)


Server()
