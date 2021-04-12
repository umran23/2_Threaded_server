import socket


class Client:
    addr = 'localhost'
    port = 3030
    connections = 4

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sock = socket.socket()
        self.port, self.addr = self.ask_for_port_addr()
        self.cleaning()
        try:
            self.sock.connect((self.addr, self.port))
            self.logging(f' connected to {self.addr}:{self.port}')
            self.main()
        finally:
            self.sock.close()

    @staticmethod
    def logging(data):
        with open("log_client.txt", "a") as f:
            f.write(f'{data}\n')

    def cleaning(self):
        with open("log_client.txt", "a") as f:
            f.write(f'\n{self.addr}, {self.port}')

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
        user_port = input("Enter Port :")
        if self.for_port(user_port) is False:
            print(f'Wrong input, Port by Default is : -  {self.port}')
            user_port = str(self.port)

        user_ip = input("Введите ip сервера:")
        if self.for_ip(user_ip) is False:
            print(f'Wrong Input, Server IP by default is : -  {self.addr}')
            user_ip = self.addr
        return int(user_port), user_ip

    def send(self, message):
        assert len(message) <= 1024
        self.logging(f'Sending this message {message}')
        self.sock.send(f'{message}'.encode())

    def recv(self):
        received = self.sock.recv(1024).decode()
        self.logging(f'Receiving a message => {received}')
        return received

    def main(self):
        message = ''
        while message != 'exit':
            message = input('<= ')
            self.send(message)
            print('=>', self.recv())


Client()
