"""
Connect
"""
import socket
import json

class Conn:
    """
    Connect to socket
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
        self.__host = host
        self.__port = port
        self.__dbconn = dbconn
        self.__skt = socket.socket(
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )
        self.__logger = logger

    @classmethod
    def __get_stream(cls, conn: object) -> dict:
        """
        Gets info from recv and decodes it as JSON
        @param conn : socket
        @return dict
        """
        try:
            stream = json.loads(conn.recv(1024).decode("utf8"))
        except json.decoder.JSONDecodeError:
            return None
        return stream

    def prepare_message(self, message: str, recipient: str, sender: str):
        self.__prepared_message = {
            'command': 'send',
            'user': sender,
            'message': message
        }

    def prepare_identity(self, user, pk, sport):
        self.__user = user
        self.__pk = pk
        self.__sport = sport

    def send_to(self, info: dict, recipient: socket.socket) -> bool:
        """
        Send info formatted as JSON with separator to connection
        @param info: dict
        @param recipient: socket.socket
        @return bool
        """
        try:
            recipient.send((json.dumps(info)+'\0').encode("utf8"))
            return True
        except json.decoder.JSONDecodeError:
            return False

    def __action(self):
        if self.__prepared_message is None:
            nmessage = {
                'command': 'connect',
                'user': self.__user,
                'pk': self.__pk,
                'sport': self.__sport
            }
            self.send_to(nmessage, self.__skt)
            data = self.__get_stream(self.__skt)
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
                self.__sport
            )
            self.__dbconn.insert(user, "user")
            self.__logger.debug("Now connected to %s", data['code'])
            return True
        else:
            self.send_to(self.__prepared_message, self.__skt)
        return False

    def __sending(self):
        # self.__skt.send("You should receive this".encode("utf8"))
        self.__logger.debug("Connecting to server")
        self.__action()
        # self.get_stream(self.__skt)
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
            self.__logger.debug("Establishing connection to %s:%s", self.__host, self.__port)
        except OSError:
            return False
        # return self.__skt
        self.__sending()
