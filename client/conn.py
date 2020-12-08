"""
Conn file, class for manage connection to servers
"""
import socket
from utils import ScktUtils


class Conn(ScktUtils):
    """
    Connect to socket class
    """
    __servers = {}
    __prepared_message: dict = None
    __user: str = ""
    __pk: str = ''
    __sport: int = None

    def __init__(
        self,
        host,
        port,
        dbconn,
        logger
    ):
        """

        @param host: Server's hostname
        @type host: str
        @param port: Server's port
        @type port: int
        @param dbconn: Database connection
        @type dbconn: object
        @param logger: Configured Logger instance
        @type logger: logging.Logger
        """
        self.__host = host
        self.__port = port
        self.__dbconn = dbconn
        self.__skt = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )
        self.__logger = logger

    def prepare_message(self, message: str, recipient: str, sender: str):
        """
        Function to prepare a message to be sent to server, and assign it to
        self.__prepared_message
        @param message: Message body
        @type message: str
        @param recipient: Recipient name
        @type recipient: str
        @param sender: Sender name
        @type sender: str
        """
        self.__prepared_message = {
            "command": "send",
            "user": sender,
            "message": message
        }

    def prepare_identity(self, user, pk, sport):
        """
        Prepare identity info to be sent to client
        as connect response
        @param user: username
        @type user: str
        @param pk: public key
        @type pk: str
        @param sport: Client's Server port, where client listens requests
        @type sport: int
        """
        self.__user = user
        self.__pk = pk
        self.__sport = sport

    def __action(self):
        """
        Executes requests, based on instance configuration
        If a message is prepared it will try to send it
        if not then it'll try to connect to server and
        wait for a response
        """
        if self.__prepared_message is None:
            nmessage = {
                "command": "connect",
                "user": self.__user,
                "pk": self.__pk,
                "sport": self.__sport
            }
            self._send_to(nmessage, self.__skt)
            data = self._get_stream(self.__skt)
            if data is None:
                return False
            if data['code'] == 0:
                self.__logger.debug(
                    "Connection refused %s",
                    data['message']
                )
                return False
            user = (
                data['user'],
                self.__host,
                data['pk'],
                data["port"]
            )
            self.__dbconn.insert(user, "user")
            self.__logger.debug("Now connected to %s", data['user'])
            return True
        else:
            self._send_to(self.__prepared_message, self.__skt)
        return False

    def __sending(self):
        """
        This function was declared to manage requests to be sent to server
        currently only executes action
        """
        self.__action()
        self.__skt.shutdown(0)
        self.__skt.close()

    def connect(self):
        """
        Intenta conectarse al socket por host y puerto
        Si la conexion fue exitosa, retorna True
        @return: bool
        """
        self.__logger.debug("connecting to %s:%i", self.__host, self.__port)
        try:
            self.__skt.connect((self.__host, self.__port))
        except OSError:
            self.__logger.debug("cannot connect to %s:%i", self.__host, self.__port)
            return False
        self.__sending()
