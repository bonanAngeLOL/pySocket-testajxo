import socket
import logging


class Conn:
    """
    Clase para conectarse a un socket
    """
    __status: bool = False

    def __init__(
            self,
            host: str,
            port: int,
            logger: logging.Logger = logging.getLogger(),
            skt: socket.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ):
        """
        @param host: str
        @param port: int
        @param logger: logging.Logger
        @param skt: socket.socket
        """
        self.host = host
        self.port = port
        self.__skt = skt
        self.__logger = logger

    def __del__(self):
        """
        Termina la conexion con el destructor
        @return:
        """
        if not self.__status:
            return False
        self.__skt.shutdown(0)
        self.__skt.close()
        return True

    @property
    def connected(self) -> bool:
        """
        Getter de __status
        @return: bool
        """
        return self.__status

    def connect(self) -> bool:
        """
        Intenta conectarse al socket por host y puerto
        Si la conexion fue exitosa, retorna True
        @return: bool
        """
        try:
            self.__skt.connect((self.host, self.port))
            self.__status = True
            self.__logger.debug("connected")
        except OSError:
            self.__status = False
        return self.__status

    def send(self, messages: list):
        """
        Envia la cada posicion en la lista como un mensaje
        @param messages: list
        @return:
        """
        for message in messages:
            message = str(message)
            self.__skt.sendall(message.encode("utf8"))
            self.__logger.debug("Sent:\t%s", message)
            data = self.__skt.recv(1024)
            self.__logger.debug("Received:\t%s\n", data)
