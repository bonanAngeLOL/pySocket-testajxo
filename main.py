"""
socket
"""
import cmd
from multiprocessing import Process
from os import path, remove
import logging
import sys
import readline
import threading
import datetime

from client.conn import Conn
from server.start import Server
from utils.db import SqliteConn
from utils.crypto import crypto, ECCcrypt


class Init(cmd.Cmd):
    """
    Init class
    """
    __logger: logging.Logger
    intro = """Type a command to start or connect to host
                \n Start a server before anything else"""
    __user = None
    __sport = None
    __dbname = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    __pubk: None
    __privk: None

    def __init__(
                self,
                logger: logging.Logger = logging.getLogger(),
                dbconn: SqliteConn = SqliteConn(
                    __dbname
                ),
                crypt_util: crypto = ECCcrypt()
            ):
        """
        @param logger: configured Logging options
        @type logger: logging.Logger
        @param dbconn: Database connection
        @type dbconn: object
        """
        super().__init__()
        self.__crypt_util = crypt_util
        self.__logger = logger
        self.prompt = " ~> "
        self.__histfile = path.expanduser('~/.babilu_history')
        self.__histfile_size = 1000
        self.__dbconn = dbconn
        self.__pubk, self.__privk = self.__crypt_util.get_keys()

    def __del__(self):
        remove(self.__dbname)

    def set_logger(self, logger: logging.Logger):
        """
        Set a logger instance
        Logger setter
        @param: logger
        @type: logging.Logger
        """
        self.__logger = logger

    @staticmethod
    def get_params(args) -> list:
        """
        Getting list of params from string
        @param args: Arguments from command line
        @type args: str
        @return list
        """
        return args.split(" ")

    @staticmethod
    def check_port(port: str) -> bool:
        """
        Check if port is numeric.
        @param port: Avilable port for binding
        @type port: str
        @return: bool
        """
        if isinstance(port, int):
            return True
        return port.isdigit()

    def init(self, host, port, user=__user) -> bool:
        """
        Init as server
        @param host: IP of host
        @type host str
        @param port: An available port
        @type port: int
        @param user: User name
        @type user: str
        @return bool
        """
        if not self.check_port(port):
            self.__logger.debug('Invalid port')
            return False
        if user is None:
            self.__logger.debug("Username required")
            return False
        self.__sport = port
        self.__user = user
        self.__dbconn.insert((user, host, self.__pubk, port, ''), "user")
        proc = Process(
            target=Server(
                host,
                int(port),
                user,
                self.__privk,
                self.__dbconn,
                self.__logger
            ).start,
            daemon=True
        )
        proc.start()
        return True

    def do_init(self, line):
        """
        init - Start a server socket to listen message requests

            use:
                python cmd: ~> init [host] [port] [username]
                bash: $ python3 main.py init [host] [port] [username]

            example:
                python cmd -> init 192.168.0.100 8090 Oscar
                bash: $ python3 main.py init 192.168.0.100 8090 Oscar

            @param line: arguments from Cmd

            host: IP address of current's object server
            port: Available port where server will be listening
            username: str

            When you try to start a server, you'll be notified if port
            was successfully binded. e.g.:

                Now listening on 192.168.0.21:8095

            If port, address or anything else prevents this program to bind
            a port you'll get an error.

                Either you don't have permission or
                port is already in use.
                Try a different port!
        """
        # Start server
        param = self.get_params(line)
        if len(param) != 3:
            raise TypeError
        self.init(*param)

    def do_send(self, recipient: str) -> bool:
        """
        send - Send a message to server

            use:
                ~> send [server username]

            example:
                ~> send oscar

            @param recipient: name of recipient (to be queried to database)
            @type recipient: str
            @return: bool

            After send command is executed you'll be asked to type a
            message to be sent, to send that message just press Enter key. e.g.

            ~> send julia
            Write a message
            [Input a message] + Enter

            To list all available servers type "send " + <Tab>
            Using tabulator will display a list of current servers. e.g.:

            ~> send <TAB>
            angel   juan    julia   pancho

            Trying to message a non connected server will lead to error
            ~> send ana
                You're not connected to ana

        """
        user = self.__dbconn.get_user_by_name(recipient)
        if user is None:
            self.__logger.debug("You're not connected to %s", recipient)
            return False
        client = Conn(user[2], user[4], self.__dbconn, self.__logger)
        client.prepare_message(
            self.__crypt_util.crypt(
                input(
                    "Write a message\n"
                ),
                user[3]
            ),
            user[1],
            self.__user
        )
        thread = threading.Thread(
            target=client.connect,
            daemon=True
        )
        thread.start()

    def do_inbox(self, args):
        """
        Function to read messages from user
        @param args:
        @return:
        """
        messages = self.__dbconn.get_sender_messages(args)
        for message in messages:
            self.__logger.debug(
                "%s %s %s",
                message[0],
                message[1],
                self.__crypt_util.decrypt(
                    message[2],
                    self.__privk
                )
            )

    def complete_inbox(self, text, line, begidx, endidx):
        """
        Function to autocomplete names in inbox command from cmd
        @param text: name or first letter from a username
        @type text: str
        @param line: str
        @param begidx: str
        @param endidx:
        """
        return self.__dbconn.get_names(text)

    def complete_send(self, text, line, begidx, endidx):
        """
        Function to autocomplete names in send command from cmd
        @param text: name or first letter from a username
        @type text: str
        @param line: str
        @param begidx: str
        @param endidx:
        """
        return self.__dbconn.get_names(text)

    def conn(self, host: str, port: int):
        """
        Connect to server
        @param host: Server's address
        @type host: str
        @param port: server's port
        @type port: int
        @return:
        """
        if not self.check_port(port):
            self.__logger.debug('Invalid port')
            return False
        client = Conn(host, int(port), self.__dbconn, self.__logger)
        client.prepare_identity(self.__user, self.__pubk, self.__sport)
        thread = threading.Thread(
            target=client.connect,
            daemon=True
        )
        thread.start()

    def do_conn(self, args):
        """
        conn - Connect to a Server from CMD:

            Use:
                ~> conn [host] [port]
            Example
                ~> conn 192.168.0.1 8085

            host: Server's Hostname or IP
            port: Server's port
            @param args: Arguments from cmd
            @type args: str

            When you try to connect a message will be displayed
            to make you know that it is attempting to connect to server
            e.g.:
                connecting to 192.168.0.21:8091

            If a connection was successful, you (and server), will be
            notified, e.g.:
                Now connected to [server's username]
        """
        param = self.get_params(args)
        if len(param) < 2:
            raise TypeError
        self.conn(param[0], int(param[1]))

    # Overwritten functions from cmd class
    def console(self):
        self.cmdloop()

    def onecmd(self, line):
        try:
            return super().onecmd(line)
        except TypeError as err:
            self.__logger.debug("%s", "Invalid arguments")
            self.__logger.debug("%s", err)
            import traceback
            traceback.print_exc()
            return False

    def emptyline(self):
        pass

    def preloop(self):
        if readline and path.exists(self.__histfile):
            readline.read_history_file(self.__histfile)

    def postloop(self):
        if readline:
            readline.set_history_length(self.__histfile_size)
            readline.write_history_file(self.__histfile)

    def do_EOF(self, args):
        """
        Exit from cmdloop
        Also available by pressing Ctrl + d
        @param args: arguments
        @type args: str
        @return:
        """
        return True

    def do_exit(self, args):
        """
        Exit from cmdloop
        @param args: arguments
        @type args: str
        """
        return self.do_EOF(args)


if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG, format="\t%(message)s")
    init = Init(logging.getLogger('socket'))
    try:
        NARGS = len(sys.argv)
        if NARGS > 1:
            init.onecmd(' '.join(sys.argv[1:]))
            if sys.argv[1] != 'help':
                init.cmdloop()
        else:
            init.cmdloop()
    except KeyboardInterrupt:
        # On ^c, closing cmdloop properly
        init.do_EOF("")
