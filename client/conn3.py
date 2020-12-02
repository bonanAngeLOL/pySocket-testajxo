"""
Connect
"""
import socket


class Conn:
    """
    Connect to socket
    """
    __servers = {}

    def __init__(
        self,
        host,
        port,
        logger
    ):
        self.__host = host
        self.__port = port
        self.__skt = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )
        self.__logger = logger

    def __del__(self):
        self.__skt.shutdown(0)
        self.__skt.close()

    def get_stream(self, conn: object):
        return conn.recv(1024).decode("utf8")

    def listen(self):
        return self.get_stream(self.__skt)

    def connect(self):
        """
        Intenta conectarse al socket por host y puerto
        Si la conexion fue exitosa, retorna True
        @return: bool
        """
        try:
            print("Waiting for response")
            self.__skt.connect((self.__host, self.__port))
            self.__logger.debug("connected")
        except OSError:
            return False
        return self.__skt
