import socket
import logging
import json
import sys

class Conn:
    """
    Clase para conectarse a un socket
    """
    __status: bool = False
    __users: []

    def __init__(
            self,
            host: str,
            port: int,
            username: str,
            password: str,
            logger: logging.Logger = logging.getLogger(),
            skt: socket.socket  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            ):
        """
        @param host: str
        @param port: int
        @param username: str
        @param password: str
        @param logger: logging.Logger
        @param skt: socket.socket
        """
        self.host = host
        self.port = port
        self.__skt = skt
        self.__logger = logger
        self.__username = username
        self.__password = password
        self.__token = ''

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

    def __get_stream(self, conn: object):
        """
        Gets info from recv and decodes it as JSON
        @param conn : socket
        @return dict
        """
        stream = {}
        received = (conn.recv(1024).decode("utf8")).split("\0")
        print("Received string", received)
        for message in received:
            if len(message) < 0 :
                continue
            print("Message to form", message)
            try:
                json_mess = json.loads(message)
            except Exception:
                continue
            print("jwon_ess", json_mess)
            if "users" in json_mess.keys():
                print("User list received")
                self.__users = message
            else:
                stream = json_mess
        return stream

    def __auth_step(self) -> bool:
        user = {
                "username":self.__username,
                "password":self.__password,
                "command":"connect"
               }
        self.__skt.send(json.dumps(user).encode("utf8"))
        message = self.__get_stream(self.__skt)
        print("Auth message ", message)
        if 'connected' in message.keys():
            if message['connected'] == 'ok':
                self.__token = message["token"]
                return True
        return False

    def __commander(self, command):
        if command == 'send':
            recipient = input("Recipient: ")
            message = input("Message :\n")
            emmit = {
                    'command': 'send',
                    'recipient': recipient,
                    'message': message
            }
            print("Sending")
            self.__skt.send(json.dumps(emmit).encode("utf8"))
            print("Sent!")

    def connect(self) -> bool:
        """
        Intenta conectarse al socket por host y puerto
        Si la conexion fue exitosa, retorna True
        @return: bool
        """
        try:
            self.__skt.connect((self.host, self.port))
            if not self.__auth_step():
                print("Auth failed")
                return False
            self.__status = True
            self.__logger.debug("connected")
        except OSError:
            self.__status = False
        while(True):
            from_server = self.__get_stream(self.__skt)
            print("received", from_server)
            command = input("Enter a command\n")
            if(command == 'exit'):
                break
            self.__commander(command)
        return self.__status

    def send(self, messages: list):
        """
        Envia la cada posicion en la lista como un mensaje
        @param messages: list
        @return:
        """
        pass
        # for message in messages:
        #    message = str(message)
        #    self.__skt.sendall(message.encode("utf8"))
        #    self.__logger.debug("Sent:\t%s", message)
        #    data = self.__skt.recv(1024)
        #    self.__logger.debug("Received:\t%s\n", data)
