import socket


class conn:

    def __init__(
            self, 
            host: str, 
            port: int, 
            skt: socket.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ):
        self.host = host
        self.port = port
        self.skt = skt
        self.connect()

    def __del__(self):
        self.skt.shutdown(0)
        self.skt.close()

    def send_async(self, message: str):
        self.skt.sendall(message.encode('utf8'))

    def connect(self):
        self.skt.connect((self.host, self.port))

    def send(self, messages: list):
        print("con ", messages)
        for message in messages:
            message = str(message)
            self.skt.sendall(message.encode("utf8"))
            print(f"Sent:\t{message}")
            data = self.skt.recv(1024)
            print(f"Received:\t{data}\n")
        return True

