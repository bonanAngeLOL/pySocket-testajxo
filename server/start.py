"""
Socket servidor
"""

import socket
import json

from concurrent.futures import ThreadPoolExecutor


class Server:

    def __init__(
        self,
        host,
        port,
        user,
        dbconn,
        logger
    ):
        self.__host = host
        self.__port = port
        self.__user = user
        self.__dbconn = dbconn
        self.__logger = logger
        self.__skt = socket.socket(
                        socket.AF_INET, socket.SOCK_STREAM
                     )

    def __def__(self):
        self.__skt.close()

    def listen_client(self, conn, addr):
        """
        Listening to client
        """
        while True:
            message = self.__get_stream(conn)
            print("From:\t", addr, f"\nmessage: \n{message}")

    def add_user(self, ip, port, username):
        """
        Set user
        """
        self.__usuarios[username] = (ip, port)

    @classmethod
    def __get_stream(cls, conn: object) -> dict:
        """
        Gets info from recv and decodes it as JSON
        @param conn : socket
        @return dict
        """
        try:
            received = conn.recv(1024).decode("utf8")
            print("received", received)
            stream = json.loads(received)
        except json.decoder.JSONDecodeError:
            print("Getting an error here in json")
            return None
        return stream

    def send_to(self, info: dict, recipient: socket.socket) -> bool:
        """
        Send info formatted as JSON with separator to connection
        @param info: dict
        @param recipient: socket.socket
        @return bool
        """
        try:
            recipient.send((json.dumps(info)).encode("utf8"))
            return True
        except json.decoder.JSONDecodeError:
            return False

    def action(self, conn, addr) -> bool:
        data = self.__get_stream(conn)
        if data is None or data == '':
            conn.close()
            return False
        try:
            if data['command'] == 'connect':
                user = self.__dbconn.get_user_by_name(data['user'])
                if user is not None:
                    nmessage = {
                        "command": "nmessage",
                        "message": "user already connected",
                        "code": 0
                    }
                    self.__logger.debug("User %s was already connected", data['user'])
                    self.send_to(nmessage, conn)
                    return False
                else:
                    nuser = (data["user"], addr[0], data['pk'], data["sport"])
                    self.__dbconn.insert(nuser, 'user')
                    myinfo = self.__dbconn.get_by_id(1, 'user')
                    nmessage = {
                        "command": "nmessage",
                        "message": "Welcome",
                        "pk": myinfo[3],
                        "user": myinfo[1],
                        "port": self.__port,
                        "code": 1
                    }
                    self.__logger.debug("User %s is now connected", data['user'])
                    self.send_to(nmessage, conn)
                    return True
            if data['command'] == 'send':
                user = self.__dbconn.connected_user(data['user'], addr[0])
                if data["message"] == '':
                    self.__logger.debug("No message found in request!")
                    return False
                if user is None:
                    self.__logger.debug(
                        """%s tried to send a message from %s, 
                        but they are not connected""",
                        data['user'],
                        addr[0]
                    )
                    return False
                self.__dbconn.insert((user[0], '', data['message']), 'queue')
                self.__logger.debug(
                    "New message from %s\n%s",
                    user[1],
                    data["message"][0:10]+'...'
                )
                return True
        except TypeError:
            self.__logger.debug("Malformed request ignored!")
        return False

    def __listening(self, executor: object):
        while True:
            # Get connection
            conn, addr = self.__skt.accept()
            # Get messages
            self.__logger.debug("Request received from %s ", addr[0])
            executor.submit(self.action, conn, addr)

    def start(self) -> bool:
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
        self.__skt.listen(10)
        self.__logger.debug(
            "Now listening on %s:%i",
            self.__host,
            self.__port
        )
        with ThreadPoolExecutor(max_workers=10) as executor:
            self.__listening(executor)
        return True

