import socket
import sys
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


class Server:
    """
    Clase para iniciar el socket
    """
    __status: bool = False

    def __init__(
                self,
                port: int,
                host: str = '127.0.0.1',
                logger: logging.Logger = logging.getLogger(),
                skt: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ):
        """
        @param port: int
        @param host: str
        @param logger: logging.Logger
        @param skt: socket.socket
        """
        self.port = port
        self.host = host
        self.skt = skt
        self.__conexion: socket.socket
        self.__direccion: tuple
        self.__logger = logger

    def __del__(self):
        """
        Cierra el socket si sigue activo
        @return:
        """
        if not self.__status:
            return False
        self.__stop()

    def __stop(self):
        """
        Cierra el socket
        """
        self.__conexion.shutdown(0)
        self.__conexion.close()

    def __respond(self, message: str):
        """
        Envia una cadena a quien este conectado
        @param message: str
        """
        self.__conexion.sendall(message.encode("utf8"))

    def __listening(self):
        """
        Ciclo para escuchar y reponder a los mensajes
        De acuerdo con la tarea, regresara el numero recibido mas 15
        el ciclo termina al recibir la cadena "stop"
        """
        self.__logger.debug("Connecting: %s", self.__conexion)
        while True:
            data = self.__conexion.recv(1024).decode("utf8")
            if data != 'stop':
                self.__logger.debug("Received: %s",data)
                data = str(int(data) + 15) if data.isdigit() else data
                self.__respond(data)
            else:
                break

    def start(self) -> bool:
        """
        Inicia el socket (bind), se agrego la opcion SO_REUSEADDR para
        evitar que el puerto se quete en TIME_WAIT y se pueda repetir el
        ejercicio inmediatamente despues de terminar
        @return: bool
        """
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


"""
Socket

Este programa permite crear un socket
del lado del cliente o del lado del servidor
Dependiendo de la opcion que se pase como parametro.

sckt.py accion direccion puerto

accion:
    start : Inicia el socket
    connect : Para conectarse

"""


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

    messages = list(range(1, 16))
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
