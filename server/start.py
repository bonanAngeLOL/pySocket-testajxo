"""
Socket servidor
"""

import socket
import sys

from concurrent.futures import ThreadPoolExecutor

class Server:

    __usuarios: dict = {}

    def __init__(
        self,
        host,
        port,
        user,
        logger
    ):
        self.__host = host
        self.__port = port
        self.__user = user
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
        stream = conn.recv(1024).decode("utf8")
        return stream

    def __listening(self, executor: object):
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
            print("data ", data)
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

