"""
Socket

"""
import logging
import sys

from client.conn import Conn
from server.start import Server


class HandleSocket:
    """
        Esta clase solo es para manejar las clases start y conn
    """
    __skt: Server
    __logger: logging.Logger
    __client: Conn

    def __init__(self, _logger: logging.Logger = logging.getLogger()):
        """
        Se inyecta la instancia del logging.Logger
        @param _logger: logging.Logger
        """
        self.__logger = _logger

    @staticmethod
    def _check_port(port: str) -> bool:
        """
        Revisar si el puerto es un valor numerico
        @type port: str
        @return: bool
        """
        return port.isdigit()

    def start(self, host: str, port: int):
        """
        Iniciar el socket
        @param host: str
        @param port: int
        """
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        self.__logger.debug("Starting socket")
        self.__skt = Server(int(port), host, self.__logger)
        self.__skt.start()
        return True

    def connect(self, host: str, port: int, user: str):
        """
        Conectarse a un socket
        @param host: str
        @param port: str
        @param user: str
        @return:
        """
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        self.__logger.debug("Trying to connect")
        self.__client = Conn(host, int(port), user, self.__logger)
        return self.__client.connect()

    def send(self, _messages: list):
        """
        Esta funcion envia un mensaje cuando self.skt es
        una instancia de conn
        @param _messages: list
        """
        if isinstance(self.__skt, Conn):
            # self.__skt.send(_messages)
            pass


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="\t%(message)s")
    logger = logging.getLogger('socket')

    NARGS = len(sys.argv)

    hskt = HandleSocket(logger)

    if sys.argv[1] == 'help':
        logger.debug("Use:socket.py Action Host SPort Cport...")
        logger.debug("\tAction\tAction of socket: start | connect ")
        logger.debug("\tHost\tHostname or IP")
        logger.debug("\tPort\tServer port number")
        logger.debug("""Connect to port:\n\t
                        socket.py connect Host Port""")
        logger.debug("Start a server:\n\tsocket.py start Host Port CSport")
    elif sys.argv[1] == 'start' and NARGS == 4:
        hskt.start(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'connect' and NARGS == 4:
        if hskt.connect(sys.argv[2], sys.argv[3], sys.argv[4]):
            pass
        else:
            logger.debug("Unable to Connect\n\tTry another port or address")
    else:
        logger.debug("Invalid action \n required: [start | connect] ")

