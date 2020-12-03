"""
Connect
"""
import socket


class Conn:
    """
    Connect to socket
    """
    __servers = {}
    __status = False

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

    def get_stream(self, conn: object):
        return conn.recv(1024).decode("utf8")

    def __sending_cycle(self):
        self.__skt.send("You should receive this".encode("utf8"))
        while True:
            print("now in cycle")
            self.get_stream(self.__skt)
        # print("Write a command")
        # while True:
        #     command = input(" > ")
        #     if command == 'exit':
        #         break
        #     self.__commander(command)
        self.__skt.shutdown(0)
        self.__skt.close()

    def connect(self):
        """
        Intenta conectarse al socket por host y puerto
        Si la conexion fue exitosa, retorna True
        @return: bool
        """
        self.__logger.debug("%s", "connecting")
        try:
            print("Waiting for response")
            self.__logger.debug("%s", "waiting for response")
            self.__skt.connect((self.__host, self.__port))
            self.__logger.debug("%s %s %s", "You are now connected to", self.__host, self.__port)
        except OSError:
            return False
        # return self.__skt
        self.__sending_cycle()
