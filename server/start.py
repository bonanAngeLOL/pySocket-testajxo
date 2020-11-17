"""
    Clase para manejar el servidor
"""
import socket


class server:
    """
        Clase server
    """

    __status: bool = False

    def __init__(
                self,
                port: int,
                host: str = '127.0.0.1',
                skt: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ):
        self.port = port
        self.host = host
        self.skt = skt
        self.__conexion: socket.socket
        self.__direccion: tuple

    def _del__(self):
        if not self.__status:
            return False
        self.__stop()

    def __stop(self):
        self.__conexion.shutdown(0)
        self.__conexion.close()

    def __respond(self, message: str):
        self.__conexion.sendall(message.encode("utf8"))

    def __listening(self):
        print("Connecting: ", self.__conexion)
        while True:
            data = self.__conexion.recv(1024).decode("utf8")
            if data != 'stop':
                print(f"Received: {data}")
                data = str(int(data) + 15) if data.isdigit() else data
                self.__respond(data)
            else:
                break

    """
    def start(self):
        self.skt.bind((self.host, self.port))
        self.skt.listen()
        conexion, direccion = self.skt.accept()
        self.__listening(conexion)
    """

    def start(self):
        self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.skt.bind((self.host, self.port))
        except (OSError, PermissionError):
            print("Port unavailable\n\t"+
                    "Either you don't have permission or port is already in use.\n"
                    "Try a different port!"
                 )
            return False
        self.skt.listen()
        self.__conexion, self.__direccion = self.skt.accept()
        self.__listening()
        self.__status = True
        return True


