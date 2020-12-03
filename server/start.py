"""
Socket servidor
"""

import socket
import sys
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
            stream = json.loads(conn.recv(1024).decode("utf8"))
        except json.decoder.JSONDecodeError:
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
            recipient.send((json.dumps(info)+'\0').encode("utf8"))
            return True
        except json.decoder.JSONDecodeError:
            return False

    def action(self, data, conn, addr) -> bool:
        try:
            if data['command'] == 'connect':
                user = self.__dbconn.get_user_by_name(data['name'])
                if user is not None:
                    nmessage = {
                        'command': 'nmessage',
                        'message': 'user already connected with the same name',
                        'code': 0
                    }
                    self.send_to(nmessage, conn)
                    return False
                else:
                    nuser = (data["username"], addr[0]+self.__port, data['pk'])
                    self.__dbconn.insert
        except KeyError:
            return False

    def __listening(self, executor: object):
        print("listening...")
        while True:
            # Get connection
            conn, addr = self.__skt.accept()
            # Get messages
            self.__logger.debug("%s", "Request received")
            data = self.__get_stream(conn)
            # If no message found close the connection
            if data is None or data == '':
                conn.close()
                continue
            print("data ", data)
            self.action(data, conn, addr)
            # Listen to the client using user object to do so!
            executor.submit(self.listen_client, conn, addr)

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
        with ThreadPoolExecutor(max_workers=10) as executor:
            self.__listening(executor)
        return True

