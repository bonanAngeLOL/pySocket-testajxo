"""
Socket

Este programa permite crear un socket
del lado del cliente o del lado del servidor
Dependiendo de la opcion que se pase como parametro.

main.py accion direccion puerto

accion:
    start : Inicia el socket
    connect : Para conectarse

Para iniciar el servidor
    python main.py start [ip] [puerto]

Para conectar al servidor
    python main.py connect [ip_servidor] [puerto] [usuario] [contraseña]


El Código está desordenado por que aun estaba haciendo pruebas con el envío

El usuario se conecta al servidor y lo guarda en la lista de usuarios, luego 
notifica a los demás usuarios la lista de usuarios conectados.

El usuario puede ingresar desde consola la opción para enviar mensajes

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
        return True

    def connect(self, host: str, port: int, user: str, password: str):
        """
        Conectarse a un socket
        @param host: str
        @param port: str
        @param user: str
        @param password: str
        @return:
        """
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        self.__logger.debug("Trying to connect")
        self.__skt = Conn(host, int(port), user, password, self.__logger)
        return self.__skt.connect()

    def send(self, _messages: list):
        """
        Esta funcion envia un mensaje cuando self.skt es
        una instancia de conn
        @param _messages: list
        """
        if isinstance(self.__skt, Conn):
            self.__skt.send(_messages)


if __name__ == "__main__":

    messages = list(range(1,16))
    messages.append("stop")

    logging.basicConfig(level=logging.DEBUG, format="\t%(message)s")
    logger = logging.getLogger('socket')

    NARGS = len(sys.argv)

    hskt = HandleSocket(logger)

    if sys.argv[1] == 'help':
        logger.debug("Use:socket.py Action Host Port params...")
        logger.debug("\tAction\tAction of socket: start | connect ")
        logger.debug("\tHost\tHostname or IP")
        logger.debug("\tPort\tServer port number")
        logger.debug("Connect to port:\n\tsocket.py connect Host Port user password")
        logger.debug("Start a server:\n\tsocket.py start Host Port max_users")
    elif sys.argv[1] == 'start' and NARGS == 4:
        hskt.start(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'connect' and NARGS == 6:
        if hskt.connect(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]):
            hskt.send(messages)
        else:
            logger.debug("Unable to Connect\n\tTry another port or address")
    else:
        logger.debug("Invalid action \n required: [start | connect] ")


        """
        TODO:

        TEST this Shit
        """
