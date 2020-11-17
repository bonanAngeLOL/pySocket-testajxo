import sys
from server.start import server
from client.conn import conn


class handleSocket():

    skt: object

    def __init__(self):
        pass

    def _check_port(self, port: str) -> bool:
        return port.isdigit()

    def start(self, host: str, port: int):
        if not self._check_port(port):
            print('Invalid port')
            return False
        print("Starting socket")
        self.skt = server(int(port), host)
        self.skt.start()

    def connect(self, host: str, port: int):
        if not self._check_port(port):
            print('Invalid port')
            return False
        print("Trying to connect")
        self.skt = conn(host, int(port))
        return self.skt.connect()

    def send(self, messages: list):
        if isinstance(self.skt, conn):
            self.skt.send(messages)


if __name__ == "__main__":
    messages = list(range(1,16))
    messages.append("stop")
    nargs = len(sys.argv)
    if nargs == 1 or nargs > 4:
        print("Invalid amount of arguments \n\n 3 required: socket.py [start | connect] [host] [port]\n")
        sys.exit("Type [help] if you have any doubt")

    hskt = handleSocket()

    if sys.argv[1] == 'help':
        print("Use:socket.py Action Host Port")
        print("\tAction\tAction of socket: start | connect ")
        print("\tHost\tHostname or IP")
        print("\tPort\tServer port number")
    elif sys.argv[1] == 'start' and nargs == 4:
        hskt.start(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'connect' and nargs == 4:
        if hskt.connect(sys.argv[2], sys.argv[3]):
            hskt.send(messages)
        else:
            print("Unable to Connect\n\tTry another port or address")
    else:
        print("Invalid action \n required: [start | connect] ")


"""
ToDo:
    Clean this code
"""
