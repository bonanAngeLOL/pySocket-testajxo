"""
    Este archivo contiene la clase que manejara los sockets
"""
import json
import logging
import socket
import sys
import os
from concurrent.futures import ThreadPoolExecutor

from utils.user import User


class Server:
    """
    Clase para iniciar el socket
    """
    __status: bool = False
    __usuarios: dict = {}

    def __init__(
                self,
                port: int,
                host: str = '127.0.0.1',
                logger: logging.Logger = logging.getLogger(),
                skt: socket.socket = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM
                    )
                ):
        """
        @param port: int
        @param host: str
        @param logger: logging.Logger
        @param skt: socket.socket
        """
        self.__port = port
        self.__host = host
        self.__logger = logger
        self.__skt = skt
        self.__direccion: tuple
        self.__client: object

    def __del__(self):
        """
        Cierra el socket si sigue activo
        @return:
        """
        self.__skt.close()

    def __get_all_users(self) -> dict:
        """
        Lista de usuarios que han iniciado sesión
        @return dict
        """
        return {'users': (list(self.__usuarios.keys()))}

    def __broadcast(self, message: dict):
        """
        Envia un mensaje a todos los usuarios
        @param message: dict
        """
        for user in self.__usuarios:
            self.send_to(message, self.__usuarios[user].get_conn())

    def auth(self, username, password) -> str:
        """
        TODO:
            - Autenticar a un usuario
            - Generar un token
        @param: username: string
        @param: password: string
        @return str
        """
        return True

    def connect_client(
                self,
                data: dict,
                addr: tuple
            ) -> bool:
        """
        Waits for clients to connect and avoids a users "connecting" twice or
        more
        ToDo:
            Validate authenticated users
        @param data: str
        @param conn: socket.socket
        @param addr: str
        @return User
        """
        try:
            cport = int(data['cport'])
            # gettin key
            # p_k = data['p_k']
        except KeyError:
            return False
        except ValueError:
            return False
        from client.conn import Conn
        self.__client = Conn(addr[0], cport, "A", self.__logger)
        return self.__client.connect()
        """
        try:
            token = self.auth(data['username'], data['password'])
        except KeyError:
            return None
        # Add control for failed token creation
        print("user ", data["username"], " token ", token)
        print("trying to create user")
        user = User(
                    data["username"],
                    data["password"],
                    token,
                    addr,
                    conn
                )
        print("User has been created", user)
        # Adding user to list of connected users
        self.__usuarios[data["username"]] = user
        print(
                "User created and attached to list",
                self.__usuarios[data['username']])
        response = {
                    'connected': 'ok',
                    # This token is provisional until auth
                    # module is finished
                    'token': ("True" if token else '')
                    }
        self.send_to(response, conn)
        print("Info sent")
        return self.__usuarios[data["username"]]
        """

    @classmethod
    def __get_stream(cls, conn: object) -> dict:
        """
        Gets info from recv and decodes it as JSON
        @param conn : socket
        @return dict
        """
        stream = {}
        try:
            stream = json.loads(conn.recv(1024).decode("utf8"))
        except json.decoder.JSONDecodeError:
            return {}
        return stream

    def __user_command(
                self,
                data: dict,
                conn: socket.socket,
            ) -> str:
        """
        Try to execute user command
        @param data: dict
        @return str
        """
        print("command received")
        try:
            print("casting command")
            if data["command"] == "send":
                print("sending")
                message = {"message": data["message"]}
                print("message formed")
                self.send_to(
                                message,
                                self.__usuarios[data["recipient"]].get_conn()
                            )
                print("message sent")
                return "done"
            if data["command"] == "stop":
                print("closing")
                conn.close()
                return "closed"
        except:
            print("Error !!!! : ", sys.exc_info()[0])
        print("getting out from commander")
        return "invalid argument"

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

    def __listen_client(self, user_conn: object):
        """
        Thread para el usuario
        @param user: User
        """
        while True:
            message = user_conn.recv(2048).decode("utf8")
            print("Received from client", message)
            try:
                print("Trying to access to commander")
                data = json.loads(message)
                print("json loaded from message", data)
                self.__user_command(data, user_conn)
            except:
                print("Error !!!! : ", sys.exc_info()[0])
                continue

    def __listening(self, executor: object):
        """
        Ciclo para escuchar y reponder a los mensajes
        De acuerdo con la tarea, regresara el numero recibido mas 15
        el ciclo termina al recibir la cadena "stop"
        @param executor : concurrent.futures.thread.ThreadPoolExecutor
        @void
        """
        while True:
            print("listening...")
            # Get connection
            conn, addr = self.__skt.accept()
            # Get messages
            print("Getting stream")
            data = self.__get_stream(conn)
            # If no message found close the connection
            if data is None or data == '':
                conn.close()
                continue
            print("New user ", data)
            # Auth user and return an User() object
            # Is user authenticated
            # Listen to the client using user object to do so!
            executor.submit(self.__listen_client, conn)
            executor.submit(self.connect_client, data, addr)

    def start(self) -> bool:
        """
        Inicia el socket (bind), se agrego la opcion SO_REUSEADDR para
        evitar que el puerto se quete en TIME_WAIT y se pueda repetir el
        ejercicio inmediatamente despues de terminar
        @return: bool
        """
        self.__skt.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            self.__skt.bind((self.__host, self.__port))
        except (OSError, PermissionError):
            message = """Port unavailable\n\t
                         Either you don't have permission or
                         port is already in use.\n
                         Try a different port!"""
            self.__logger.debug("%s", message)
            return False
        self.__skt.listen(1)
        with ThreadPoolExecutor(max_workers=10) as executor:
            self.__listening(executor)
        return True
