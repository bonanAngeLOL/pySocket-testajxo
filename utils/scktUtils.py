import json
from typing import Union


class scktUtils:

    def __init__(*arg):
        pass

    @classmethod
    def _get_stream(cls, conn: object) -> Union[dict, None]:
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

    @classmethod
    def _send_to(cls, info: dict, recipient: object) -> bool:
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
