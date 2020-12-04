"""
socket
"""
import cmd
from multiprocessing import Process
import logging
import sys
import os.path
import readline
import threading
import datetime

from client.conn import Conn
from server.start import Server
from utils.db import SqliteConn


class Init(cmd.Cmd):
    """
    Init class
    """
    __logger: logging.Logger
    intro = "Type a command to start o connect to host"
    __user = None
    __pk = 1
    __sport = None

    def __init__(
                self,
                logger: logging.Logger = logging.getLogger(),
                dbconn=SqliteConn(
                    datetime.datetime.now().strftime('%Y%m%d%H%M%S')
                )
            ):
        super().__init__()
        self.__logger = logger
        self.prompt = " ~> "
        self.__histfile = os.path.expanduser('~/.babilu_history')
        self.__histfile_size = 1000
        self.__dbconn = dbconn

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
        if isinstance(port, int):
            return True
        return port.isdigit()

    def get_params(self, line):
        """
        Getting list from string
        """
        return line.split(" ")

    def init(self, host, port, user=__user):
        """
        Init as server
        """
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        if user is None:
            self.__logger.debug("Username required")
            return False
        self.__sport = port
        self.__user = user
        # -- Start server: IP PORT USER LOGGER
        server = Server(host, int(port), user, self.__dbconn, self.__logger)
        print("server inst")
        proc = Process(
            target=server.start,
            args=(),
            daemon=True
        )
        proc.start()
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

    def do_send(self, recipient):
        user = self.__dbconn.get_user_by_name(recipient)
        if user is None:
            self.__logger.debug("You're not connected to %s", user)
            return False
        client = Conn(user[2], user[4], self.__dbconn, self.__logger)
        client.prepare_message(input("Write a message"), user[1], self.__user)

    def conn(self, host: str, port: int, user: str):
        """
        Conectarse a un socket
        @param host: str
        @param port: str
        @param user: str
        @return:
        """
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        self.__logger.debug("Trying to connect")
        client = Conn(host, int(port), self.__dbconn, self.__logger)
        client.prepare_identity(self.__user, self.__pk, self.__sport)
        print(client)
        thread = threading.Thread(
            target=client.connect,
            daemon=True
        )
        thread.start()

    def do_conn(self, args):
        param = self.get_params(args)
        if len(param) < 3:
            raise TypeError
        self.conn(param[0], int(param[1]), param[2])

    def do_setuser(self, args):
        param = self.get_params(args)
        if len(param) != 1:
            raise TypeError
        self.__user = args[0]

    def console(self):
        self.cmdloop()

    def onecmd(self, line):
        try:
            return super().onecmd(line)
        except TypeError as err:
            self.__logger.debug("%s", "Invalid arguments")
            self.__logger.debug("%s", err)
            return False

    def emptyline(self):
        pass

    def preloop(self):
        if readline and os.path.exists(self.__histfile):
            readline.read_history_file(self.__histfile)

    def postloop(self):
        if readline:
            readline.set_history_length(self.__histfile_size)
            readline.write_history_file(self.__histfile)

    def do_EOF(self, line):
        return True

    def do_exit(self, line):
        return self.do_EOF(line)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="\t%(message)s")
    # init.set_logger(logging.getLogger('socket')) NOT REQUIRED YET

    init = Init(logging.getLogger('socket'))

    NARGS = len(sys.argv)

    if NARGS > 1:
        init.onecmd(' '.join(sys.argv[1:]))
        init.cmdloop()
    else:
        init.cmdloop()
