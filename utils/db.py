import sqlite3


class SqliteHandler:
    """
    Clase para manejar los registros con SQLite
    """
    __users: str = """CREATE TABLE IF NOT EXISTS users_test (
                        id_u INTEGER PRIMARY KEY,
                        username TEXT,
                        addr TEXT NOT NULL,
                        public_k TEXT NOT NULL
                    );"""

    __messages: str = """CREATE TABLE IF NOT EXISTS queue
                         id_q INTEGER PRIMARY KEY,
                         sender TEXT,
                         recipient TEXT NOT NULL,
                         message TEXT NOT NULL,
                         timest DEFAULT CURRENT_TIMESTAMP
                        );"""

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

    def insert(self, params: tuple) -> int:
        """
        Insertar un registro en la base de datos, regresa el Id de registro

        @param params : tuple
        @return: int
        """
        self.__run_query("""INSERT INTO users_test
                        (nombre, apellidos, contrasena, email) values
                        (?, ?, ?, ?)""", params)
        return self.__cursor.lastrowid

    def get_by_id(self, id: int) -> tuple:
        """
        Obtener un registro mediante en ID

        @param id: int
        @return tuple
        """
        result = self.__run_query("""SELECT * FROM
                 users_test where id = ?""", (id, ))
        if len(result) > 0:
            return result[0]
        return None

    def get_all(self) -> list:
        """
        Obtener todos los registros de una tabla

        @return list
        """
        return self.__run_query("SELECT * FROM users_test")

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


if __name__ == '__main__':
    print("Tarea Base de datos")
    # Sqlite class
    db = SqliteHandler("test")

    # Usuarios
    user1 = ("Juan", "Perez", "password1", "juan@perez.com",)
    user2 = ("Pedro", "C.", "contraseña", "pedro@c.com",)

    # Insertar usuarios
    db.insert(user1)
    pedroId = db.insert(user2)

    # Id de pedro
    print("Id de pedro", pedroId)

    # Consulta a pedro por su Id
    pedro = db.get_by_id(pedroId)

    # Información de pedro
    print("pedro", pedro)

    # Todos los usuarios registrados
    users = db.get_all()
    print("All ", users)
