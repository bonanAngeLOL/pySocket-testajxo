"""
    Clase para manejar el servidor
"""
import socket
import logging

class server:
    """
        Clase server
    """

    __status: bool = False

    def __init__(
                self,
                port: int,
                host: str = '127.0.0.1',
                logger: logging.Logger = logging.getLogger(),
                skt: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ):
        self.port = port
        self.host = host
        self.skt = skt
        self.__conexion: socket.socket
        self.__direccion: tuple
        self.__logger = logger

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
        self.__logger.debug("Connecting: %s", self.__conexion)
        while True:
            data = self.__conexion.recv(1024).decode("utf8")
            if data != 'stop':
                self.__logger.debug("Received: %s",data)
                data = str(int(data) + 15) if data.isdigit() else data
                self.__respond(data)
            else:
                break

    def start(self):
        self.skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.skt.bind((self.host, self.port))
        except (OSError, PermissionError):
            message = """Port unavailable\n\t
                         Either you don't have permission or port is already in use.\n
                         Try a different port!"""
            self.__logger.debug("%s", message)
            return False
        self.skt.listen()
        self.__conexion, self.__direccion = self.skt.accept()
        self.__listening()
        self.__status = True
        return True


