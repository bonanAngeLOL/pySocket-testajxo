"""
Socket

Este programa permite crear un socket
del lado del cliente o del lado del servidor
Dependiendo de la opcion que se pase como parametro.

socket.py accion direccion puerto

accion:
    start : Inicia el socket
    connect : Para conectarse

"""
import sys
import logging
from server.start import Server
from client.conn import Conn


class HandleSocket:
    """
        Esta clase solo es para manejar las clases start y conn
    """
    __skt: object
    __logger: logging.Logger

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

    def connect(self, host: str, port: int):
        """
        Conectarse a un socket
        @param host:
        @param port:
        @return:
        """
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        self.__logger.debug("Trying to connect")
        self.__skt = Conn(host, int(port), self.__logger)
        return self.__skt.connect()

    def send(self, messages: list):
        """
        Esta funcion envia un mensaje cuando self.skt es
        una instancia de conn
        @param messages: list
        """
        if isinstance(self.__skt, Conn):
            self.__skt.send(messages)


if __name__ == "__main__":

    messages = list(range(1,16))
    messages.append("stop")

    logging.basicConfig(level=logging.DEBUG, format="\t%(message)s")
    logger = logging.getLogger('socket')

    NARGS = len(sys.argv)
    if NARGS == 1 or NARGS > 4:
        logger.debug("Invalid amount of arguments \n\n 3 required: socket.py [start | connect] [host] [port]\n")
        sys.exit("Type [help] if you have any doubt")

    hskt = HandleSocket(logger)

    if sys.argv[1] == 'help':
        logger.debug("Use:socket.py Action Host Port")
        logger.debug("\tAction\tAction of socket: start | connect ")
        logger.debug("\tHost\tHostname or IP")
        logger.debug("\tPort\tServer port number")
    elif sys.argv[1] == 'start' and NARGS == 4:
        hskt.start(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'connect' and NARGS == 4:
        if hskt.connect(sys.argv[2], sys.argv[3]):
            hskt.send(messages)
        else:
            logger.debug("Unable to Connect\n\tTry another port or address")
    else:
        logger.debug("Invalid action \n required: [start | connect] ")
