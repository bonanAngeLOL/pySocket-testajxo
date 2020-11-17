import sys
import logging
from server.start import server
from client.conn import conn


class handleSocket():

    skt: object
    __logger: logging.Logger

    def __init__(self, _logger: logging.Logger = logging.getLogger()):
        self.__logger = _logger

    def _check_port(self, port: str) -> bool:
        return port.isdigit()

    def start(self, host: str, port: int):
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        self.__logger.debug("Starting socket")
        self.skt = server(int(port), host, self.__logger)
        self.skt.start()

    def connect(self, host: str, port: int):
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        self.__logger.debug("Trying to connect")
        self.skt = conn(host, int(port), self.__logger)
        return self.skt.connect()

    def send(self, messages: list):
        if isinstance(self.skt, conn):
            self.skt.send(messages)


if __name__ == "__main__":

    messages = list(range(1,16))
    messages.append("stop")

    logging.basicConfig(level=logging.DEBUG, format="\t%(message)s")
    logger = logging.getLogger('socket')

    NARGS = len(sys.argv)
    if NARGS == 1 or NARGS > 4:
        logger.debug("Invalid amount of arguments \n\n 3 required: socket.py [start | connect] [host] [port]\n")
        sys.exit("Type [help] if you have any doubt")

    hskt = handleSocket(logger)

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


"""
ToDo:
    Clean this code
"""
