"""
Esta clase es usada para encapsular la información de los usuarios
incluyendo la sesión para usarlos desde la lista de usuarios de 

"""
class User:
    """
    Clase usuario
    """
    def __init__(self, username: str, password: str, token: str, addr: str, conn: object):
        """
        @param username: str
        @param password: str
        @param token: str
        @param addr: str
        @param conn: socket.socket
        """
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
        @return str
        """
        return self.__addr

    def get_conn(self) -> object:
        """
        Returns conn
        @return socket.socket
        """
        return self.__conn

    def get_username(self) -> str:
        """
        Return username
        @return str
        """
        return self.__username


