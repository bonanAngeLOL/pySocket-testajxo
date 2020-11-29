"""
    Este archivo contiene la clase que manejara los sockets
"""
import socket
import logging
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor

class User:
    """
    Clase usuario
    """
    def __init__(self, username: str, password: str, token: str, addr: str, conn: socket.socket):
        self.__username = username
        self.__password = password
        self.__token = token
        self.__addr = addr
        self.__conn = conn

    def get_token(self) -> str:
        """
        Returns session token
        @return str
        """
        return self.__token

    def get_addr(self) -> str:
        """
        Returns addr
        """
        return self.__addr

    def get_conn(self) -> socket.socket:
        """
        Returns conn
        """
        return self.__conn

    def get_username(self) -> str:
        """
        Return username
        """
        return self.__username


class Server:
    """
    Clase para iniciar el socket
    """
    __status: bool = False
    __usuarios:dict = {}
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
        self.__port = port
        self.__host = host
        self.__logger = logger
        self.__skt = skt
        self.__direccion: tuple

    def __del__(self):
        """
        Cierra el socket si sigue activo
        @return:
        """
        if not self.__status:
            return False
        self.__skt.close()
        return True

    #def __stop(self, conn):
    #    """
    #    Cierra el socket
    #    """
    #    self.__conexion.shutdown(0)
    #    self.__conexion.close()

    def __get_all_users(self) -> str:
        return json.dumps({'users':(list(self.__usuarios.keys()))})

    def __broadcast(self, message: str):
        """
        Envia un mensaje a todos los usuarios
        @param message: str
        """
        for user in self.__usuarios:
            print(self.__usuarios[user])
            self.__usuarios[user].get_conn().send(message)

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

    def connect_client(self, data: dict, conn: socket.socket, addr: str) -> User:
        """
        Waits for clients to connect and avoids a users "connecting" twice or more
        ToDo:
            Validate authenticated users
        @param data: str
        @param conn: socket.socket
        @param addr: str
        @return User
        """
        if data["username"] in self.__usuarios:
            print("user already loged in?")
            # Need to compare a token, disconect if user is not auth
            if data['username'] in self.__usuarios.keys():
                print("\tReturning to session")
                return self.__usuarios[data["username"]]
        else:
            token = self.auth(data['username'], data['password'])
            print("user ", data["username"], " token ", token)
            if token:
                try:
                    print("Token True")
                    print("trying to create user")
                    user = ''
                    user = User(
                                data["username"],
                                data["password"],
                                token,
                                addr,
                                conn
                                )
                    print("User has been created", user)
                    self.__usuarios[data["username"]] = user
                    print("User created and attached to list", self.__usuarios[data['username']])
                    try:
                        response = {
                                    'connected':'ok',
                                    'token': ("True" if token else '')
                                    }
                        conn.send((json.dumps(response)+"|").encode("utf8"))
                    except:
                        e = sys.exc_info()
                        print(e)
                    print("Info sent")
                    return self.__usuarios[data["username"]]
                except TypeError:
                    return None
        conn.send("{'connected':'refused'}|".encode("utf8"))
        return None

    @classmethod
    def __get_stream(cls, conn: object):
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

    def __user_command(self, data: dict, conn: socket.socket, username: str) -> str:
        """
        Try to execute user command
        @param data: dict
        @return str
        """
        if data["command"] == "send":
            message = json.dumps({"sender":username, "message":data["message"]})+"|"
            self.__usuarios[data["recipient"]].get_conn.send(message.encode("utf8"))
            return "done"
        if data["command"] == "stop":
            conn.close()
            return "closed"
        return "invalid argument"

    def __listen_client(self, user: User):
        """
        Thread para el usuario
        @param user: User
        """
        while True:
            print("listening user...")
            user_conn = user.get_conn()
            print("sent keepalive")
            user_conn.send(json.dumps({'connected':'ok'}).encode("utf8"))
            print("Waiting for response")
            message = user_conn.recv(2048).decode("utf8")
            print(message)
            try:
                data = json.loads(message)
                self.__user_command(data, user_conn, user_conn.get_username())
            except json.decoder.JSONDecodeError:
                print("Error!")
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
            try:
                user = self.connect_client(data, conn, addr)
            except KeyError:
                conn.close()
                print("Malformed request received")
                continue
            # Is user authenticated
            if user is None:
                # They wasn't
                conn.close()
                continue
            # Send a list of connected users to all connected users
            self.__broadcast((self.__get_all_users()+"|").encode("utf8"))
            # Listen to the client using user object to do so!
            executor.submit(self.__listen_client, user)

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
                         Either you don't have permission or port is already in use.\n
                         Try a different port!"""
            self.__logger.debug("%s", message)
            return False
        self.__skt.listen(10)
        with ThreadPoolExecutor(max_workers=1) as executor:
            self.__listening(executor)
        return True
