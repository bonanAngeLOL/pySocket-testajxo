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
        """
        @param logger: configured Logging options
        @type logger: logging.Logger
        @param dbconn: Database connection
        @type dbconn: object
        """
        super().__init__()
        self.__logger = logger
        self.prompt = " ~> "
        self.__histfile = os.path.expanduser('~/.babilu_history')
        self.__histfile_size = 1000
        self.__dbconn = dbconn

    def set_logger(self, logger: object):
        """
        Set a logger instance
        Logger setter
        @param: logger
        @type: logging.Logger
        """
        self.__logger = logger

    @staticmethod
    def _check_port(port: str) -> bool:
        """
        Check if port is numeric.
        @param port: Avilable port for binding
        @type port: str
        @return: bool
        """
        if isinstance(port, int):
            return True
        return port.isdigit()

    def get_params(self, args):
        """
        Getting list of params from string
        @line
        """
        return args.split(" ")

    def save_user(self, conn, user_data):
        """
        Save user info in database
        @param conn: DB connection
        @type conn: obj
        @param user_data: User's info to be saved
        @type: tuple
        @return:
        """
        return conn.insert(user_data, "user")

    def init(self, host, port, user=__user):
        """
        Init as server
        @param host: IP of host
        @type host str
        @param port: An available port
        @type port: int
        @param user: User name
        @type user: str
        """
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        if user is None:
            self.__logger.debug("Username required")
            return False
        self.__sport = port
        self.__user = user
        self.save_user(self.__dbconn, (user, host, self.__pk, port))
        proc = Process(
            target=Server(
                host,
                int(port),
                user,
                self.__dbconn,
                self.__logger
            ).start,
            daemon=True
        )
        proc.start()

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
            self.__logger.debug("You're not connected to %s", recipient)
            return False
        client = Conn(user[2], user[4], self.__dbconn, self.__logger)
        client.prepare_message(input("Write a message\n"), user[1], self.__user)
        thread = threading.Thread(
            target=client.connect,
            daemon=True
        )
        thread.start()

    def complete_send(self, text, line, begidx, endidx):
        return self.__dbconn.get_names(text)

    def conn(self, host: str, port: int):
        """
        Conectarse a un socket
        @param host: str
        @param port: str
        @return:
        """
        if not self._check_port(port):
            self.__logger.debug('Invalid port')
            return False
        client = Conn(host, int(port), self.__dbconn, self.__logger)
        client.prepare_identity(self.__user, self.__pk, self.__sport)
        thread = threading.Thread(
            target=client.connect,
            daemon=True
        )
        thread.start()

    def do_conn(self, args):
        param = self.get_params(args)
        if len(param) < 2:
            raise TypeError
        self.conn(param[0], int(param[1]))

    def do_setuser(self, args):
        param = self.get_params(args)
        if len(param) != 1:
            raise TypeError
        self.__user = args[0]

    # Overwritten functions from cmd class
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

    def do_EOF(self, args):
        """
        Exit from cmdloop
        @param line: arguments
        @type line: str
        @return:
        """
        return True

    def do_exit(self, args):
        """
        Exit from cmdloop
        @param line: arguments
        @type line: str
        @return:
        """
        return self.do_EOF(args)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="\t%(message)s")
    init = Init(logging.getLogger('socket'))
    try:
        NARGS = len(sys.argv)
        if NARGS > 1:
            init.onecmd(' '.join(sys.argv[1:]))
            init.cmdloop()
        else:
            init.cmdloop()
    except KeyboardInterrupt:
        # On ^c, closing cmdloop properly
        init.do_EOF("")
