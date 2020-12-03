import sqlite3


class SqliteConn:
    """
    Clase para manejar los registros con SQLite
    """

    __user: str = """CREATE TABLE IF NOT EXISTS user (
                        id_u INTEGER PRIMARY KEY,
                        username TEXT,
                        addr TEXT NOT NULL,
                        public_k TEXT NOT NULL
                    );"""

    __queue: str = """CREATE TABLE IF NOT EXISTS queue
                         id_q INTEGER PRIMARY KEY,
                         sender INTEGER,
                         recipient INTEGER,
                         message TEXT NOT NULL,
                         timest DEFAULT CURRENT_TIMESTAMP
                        );"""

    __inserting: dict = {
        'user': """INSERT INTO user
                    (username, addr, public_k)
                    values
                    (?, ?, ?)""",
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
                    where id_q"""
    }

    def __init__(self, database: str):
        self.__conn = sqlite3.connect(database)
        self.__cursor = self.__conn.cursor()
        self.__run_query(self.__users)
        self.__run_query(self.__messages)

    def __del__(self):
        """
            Se cierra el cursor y la conexión
        """
        self.__cursor.close()
        self.__conn.close()

    def insert(self, params: tuple, table: str) -> int:
        """
        Insertar un registro en la base de datos, regresa el Id de registro

        @param params : tuple
        @param table: str
        @return: int
        """
        if table not in self.__inserting.keys():
            return 0
        self.__run_query(self.__inserting[table], params)
        return self.__cursor.lastrowid

    def get_by_id(self, idn: int, table: str) -> tuple:
        """
        Obtener un registro mediante en ID

        @param idn: int
        @param table: str
        @return tuple
        """
        if table not in self.__selecting_id():
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
        return self.__run_query("SELECT * FROM user WHERE")

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
            return None
        return self.__cursor.fetchall()
