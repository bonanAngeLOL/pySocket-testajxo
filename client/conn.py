class conn:

    def __init__(self, host: str, port: int, skt: socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)):
        self.host = host
        self.port = port
        self.skt = skt

    def send(str -> ):

    def connect():
        this.skt.connect((self.host, self.port))
        data = s.recv(1024) #Recibir respuesta

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT)) #Iniciar el socket
    s.sendall(b'hola mundo') #Enviar mensaje en formato binario
    print('Received', repr(data))  # imprimir respuesta
    s.shutdown(0)
    data = s.recv(1024)  # Recibir respuesta
    if data == '':
        s.close()

