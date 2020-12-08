import json


class ScktUtils:

    def __get_stream(self, conn: object) -> dict:
        """
        Gets info from recv and decodes it as JSON to dict
        @param conn : socket
        @return dict
        """
        try:
            received = conn.recv(1024).decode("utf8")
            stream = json.loads(received)
        except json.decoder.JSONDecodeError:
            return None
        return stream

    def send_to(self, info: dict, recipient: socket.socket) -> bool:
        """
        Send info formatted as JSON
        @param info: dict
        @param recipient: socket.socket
        @return bool
        """
        try:
            recipient.send((json.dumps(info)).encode("utf8"))
            return True
        except json.decoder.JSONDecodeError:
            return False

