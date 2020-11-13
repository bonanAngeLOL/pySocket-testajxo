
class server:
    
    def __init__(
                self, port: int, 
                host: str = '127.0.0.1', 
                socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                ):
        self.port = port
        self.host = host
        self.socket = socket

    def __listening():


    def start(self):
        self.socket.bind(self.host, self.port)
        self.listen()
        conexion, direccion = self.socket.accept()
        with conexion:
            print("conectado a ", conexion)
            while True:
                data = conexion.recv(1024)
                print("Mensaje recibido", repr(data))
                if not data:
                    conexion.shutdown(0)
                    conexion.close()
                    break
                conexion.sendall(data)

        

