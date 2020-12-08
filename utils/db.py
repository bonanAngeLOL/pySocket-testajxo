import sqlite3
from threading import Lock


class SqliteConn:
    """
    Clase para manejar los registros con SQLite
    """

    __user: str = """CREATE TABLE IF NOT EXISTS user (
                        id_u INTEGER PRIMARY KEY,
                        username TEXT,
                        addr TEXT NOT NULL,
                        public_k TEXT NOT NULL,
                        server_p INTEGER,
                        private_k TEXT DEFAULT NULL
                    );"""

    __queue: str = """CREATE TABLE IF NOT EXISTS queue(
                         id_q INTEGER PRIMARY KEY,
                         sender INTEGER,
                         recipient INTEGER,
                         message TEXT NOT NULL,
                         timest DEFAULT CURRENT_TIMESTAMP
                        );"""

    __inserting: dict = {
        'user': """INSERT INTO user
                    (username, addr, public_k, server_p, private_k)
                    values
                    (?, ?, ?, ?, ?)""",
        'queue': """INSERT INTO queue
                    (sender, recipient, message)
                    values
                    (?, ?, ?)
                    """
    }

    __selecting_id: dict = {
        'user': """SELECT * FROM user
                    where id_u = ?""",
        'queue': """SELECT * FROM queue
                    where id_q = ?"""
    }

    def __init__(self, database: str, lock: Lock = Lock()):
        """
        @param database: database name
        @type database: str
        @param lock: Lock object to protect insert
        @type lock: Lock
        """
        self.__lock = lock
        self.__conn = sqlite3.connect(database, check_same_thread=False)
        self.__cursor = self.__conn.cursor()
        self.__run_query(self.__user)
        self.__run_query(self.__queue)

    def __del__(self):
        """
            Se cierra el cursor y la conexión
        """
        self.__cursor.close()
        self.__conn.close()

    def insert(self, params: tuple, table: str) -> int:
        """
        Insertar un registro en la base de datos, regresa el Id de registro

        @param params: Information to be stored in db
        @type params: tuple
        @param table: table name
        @type table: str
        @return: int
        """
        with self.__lock:
            if table not in self.__inserting.keys():
                return 0
            self.__run_query(self.__inserting[table], params)
        return self.__cursor.lastrowid

    def get_by_id(self, idn: int, table: str) -> tuple:
        """
        Obtener un registro mediante en ID

        @param idn: Id of object
        @type idn: int
        @param table: table name
        @type table: str
        @return tuple
        """
        if table not in self.__selecting_id.keys():
            return ()
        result = self.__run_query(self.__selecting_id[table], (idn, ))
        if len(result) > 0:
            return result[0]
        return None

    def get_all(self) -> list:
        """
        Obtener todos los registros de una tabla
        @return list
        """
        return self.__run_query("SELECT * FROM users")

    def get_user_by_name(self, name: str):
        """
        Querying user info by their name
        @param name: username
        @type name: str
        @return:
        """
        result = self.__run_query(
            "SELECT * FROM user WHERE username = ?",
            (name, )
        )
        if len(result) > 0:
            return result[0]
        return None

    def connected_user(self, name: str, addr: str):
        """
        Get user information from stored users
        @param name: username
        @type name: str
        @param addr: str
        @return:
        """
        result = self.__run_query(
            "SELECT * FROM user WHERE username = ? and addr = ?",
            (name, addr)
        )
        if len(result) > 0:
            return result[0]
        return None

    def get_sender_messages(self, name):
        """
        Query a list of messages sent by an specific sender
        @param name:
        @return:
        """
        query = """ select 
                        u.username, q.timest, q.message 
                    from 
                        queue q, user u
                    where
                        u.id_u = q.sender and
                        u.username = ? and 
                        q.recipient = '';"""
        return self.__run_query(query, (name, ))

    def get_names(self, name: str) -> list:
        """
        Query a list of user whose username start with
        a given string
        @param name: username
        @return: list
        """
        return list(
            map(
                lambda name_r: name_r[0],
                self.__run_query(
                    "SELECT username FROM user WHERE username like ?",
                    (name+'%', )
                )
            )
        )

    def __run_query(self, query: str, parameters=()) -> list:
        """
        Corre una consulta de manera segura

        @param query: str
        @param parameters : tuple
        @return list
        """
        try:
            self.__cursor.execute(query, parameters)
            self.__conn.commit()
        except Exception:
            return ()
        return self.__cursor.fetchall()
