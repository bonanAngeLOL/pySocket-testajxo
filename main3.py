"""
socket
"""
import cmd
import multiprocessing
import logging
import sys
import threading

from client.conn3 import Conn
from server.start3 import Server


class Init(cmd.Cmd):
    """
    Init class
    """
    __logger: logging.Logger
    __ConnectedTo: {}

    def __init__(
                self,
                logger
            ):
        super().__init__()
        self.__logger = logger
        self.prompt = " ~> "

    def __del__(self):
        pass

    def set_logger(self, logger):
        """
        Logger setter
        """
        self.__logger = logger

    @staticmethod
    def _check_port(port: str) -> bool:
        """
        Revisar si el puerto es un valor numerico
        @type port: str
        @return: bool
        """
        return port.isdigit()

    def get_params(self, line):
        """
        Getting list from string
        """
        return line.split(" ")

    def init(self, host, port, user):
        """
        Init as server
        """
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        # -- Start server: IP PORT USER LOGGER
        server = Server(host, int(port), user, self.__logger)
        # binding ok ?
        server.start()
        self.__logger.debug(
                    "Listening now on: \n\t\t %s:%s",
                    host,
                    port
                )
        return True
        # starting server and wait for users

    def do_init(self, line):
        """
        Call to init() from python cmd
        """
        # Start server
        param = self.get_params(line)
        if len(param) != 3:
            raise TypeError
        self.init(*param)

    def listen_client(self, conn):
        while True:
            from_server = conn.recv(1024).decode("utf8")
            print(from_server)

    def conn(self, host, port, user) -> bool:
        """
        Connect to server
        """
        # start with process pool
        conn = Conn(host, port, self.__logger)
        if not conn.connect():
            raise TypeError
        multiprocessing.Process(
                    target=self.listen_client,
                    args=(conn,)
                ).start()
        return True

    def do_conn(self, args):
        param = self.get_params(args)
        if len(param) < 3:
            raise TypeError
        self.conn(param[0], int(param[1]), param[2])

    def console(self):
        self.cmdloop()

    # def onecmd(self, line):
    #    try:
    #        return super().onecmd(line)
    #    except TypeError as err:
    #        self.__logger.debug("%s", "Invalid arguments")
    #        self.__logger.debug("%s", err)
    #        return False

    def emptyline(self):
        pass


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="\t%(message)s")
    # init.set_logger(logging.getLogger('socket')) NOT REQUIRED YET

    init = Init(logging.getLogger('socket'))

    NARGS = len(sys.argv)

    if NARGS == 3:
        if sys.argv[1] == "start":
            # IP PORT USER LOGGER
            init.init(sys.argv[2], sys.argv[3], sys.argv[4])
    elif NARGS == 1:
        print("Write a command")
        init.cmdloop()
