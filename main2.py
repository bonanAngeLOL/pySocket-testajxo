"""
Socket

"""
import logging
import sys

from server.start import Server


class HandleSocket:
    """
        Esta clase solo es para manejar las clases start y conn
    """
    __skt: Server
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

    def start(self, ip: str, port: int, username: str):
        """
        Iniciar el socket
        @param host: str
        @param port: int
        """
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        self.__logger.debug("Starting socket")
        self.__skt = Server(int(port), ip, username, self.__logger)
        self.__skt.start()
        return True

    def connect(
                self,
                ip: str,
                port: int,
                user: str,
                s_ip: str,
                s_port: int,
                s_user: str
            ):
        self.__skt = Server(int(port), ip, user)
        self.__skt.add_user(s_ip, s_port, s_user)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="\t%(message)s")
    logger = logging.getLogger('socket')

    NARGS = len(sys.argv)

    hskt = HandleSocket(logger)

    if NARGS >= 1:
        if sys.argv[1] == "start":
            # IP PORT USER
            hskt.start(sys.argv[2], sys.argv[3], sys.argv[4])
        if sys.argv[1] == "connect":
            pass
