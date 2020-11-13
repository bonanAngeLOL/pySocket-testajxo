"""
import socket
from client.conn import conn
from server.start import server

def main():
    print("asdf")

if __name__ == "__main__":
    main()
"""

import socket

# create an INET, STREAMing socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# now connect to the web server on port 80 - the normal http port
s.connect(("127.0.0.1", 9090))
