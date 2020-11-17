import socket
import logging 

class conn:

    __status: bool = False

    def __init__(
            self, 
            host: str, 
            port: int, 
            logger: logging.Logger = logging.getLogger(),
            skt: socket.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ):
        self.host = host
        self.port = port
        self.__skt = skt
        self.__logger = logger

    def __del__(self):
        if not self.__status:
            return False
        self.__skt.shutdown(0)
        self.__skt.close()
        return True

    @property
    def connected(self) -> bool:
        return self.__status

    def send_async(self, message: str):
        self.__skt.sendall(message.encode('utf8'))

    def connect(self):
        try:
            self.__skt.connect((self.host, self.port))
            self.__status = True
            self.__logger.debug("connected")
        except OSError:
            self.__status = False
        return self.__status

    def send(self, messages: list):
        for message in messages:
            message = str(message)
            self.__skt.sendall(message.encode("utf8"))
            self.__logger.debug("Sent:\t%s", message)
            data = self.__skt.recv(1024)
            self.__logger.debug("Received:\t%s\n", data)
        return True

