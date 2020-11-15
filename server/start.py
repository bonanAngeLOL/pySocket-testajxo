import socket


class server:
    
    def __init__(
                self, 
                port: int, 
                host: str = '127.0.0.1', 
                skt: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ):
        self.port = port
        self.host = host
        self.skt = skt

    def __stop(self, conexion: socket.socket):
        conexion.shutdown(0)
        conexion.close()

    def __respond(self, message: str, conexion: socket.socket):
        conexion.sendall(data)

    def __listening(self, conexion: socket.socket):
        print("conectado a ", conexion)
        while True:
            data = conexion.recv(1024).decode("utf8")
            if data != 'stop':
                print(f"Mensaje recibido {data}")
                data = str(int(data) + 15) if data.isdigit() else data
                conexion.sendall(data.encode("utf8"))
            else: 
                self.__stop(conexion)
                break

    def start(self):
        self.skt.bind((self.host, self.port))
        self.skt.listen()
        conexion, direccion = self.skt.accept()
        self.__listening(conexion)

