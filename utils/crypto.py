import rsa
from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt


class crypto:
    """
    Super clase para generalizar las siguientes dos clases ECCcrypt y RSACrypt
    """
    def get_keys(self) -> tuple:
        """
        Esta funcion genera un par de llaves, publica y privada
        :return: tuple : Llaves publica y privada en una tupla (publica, privada)
        """
        pass

    def crypt(self, message: str, key: str) -> str:
        """
        Cifra un mensaje con una llave, dependiendo del algoritmo usado
        en la implementacion de esta funcion
        :param message: str : Mensaje en texto plano
        :param key: str: Llave publica del receptor
        :return: str : Mensaje cifrado
        """
        pass

    def decrypt(self, cmessage: str, key: str) -> str:
        """
        Descifra un mensaje con una llave, dependiendo del algoritmo usado
        en la implementacion de la funcion
        :param cmessage: str : Mensaje cifrado con la llave publica del receptor
        :param key: str : Llave privada del receptor
        :return: str : Mensaje descifrado
        """
        pass


class ECCcrypt(crypto):
    """
    Implentacion de Crypto() para cifrar y descifrar con ECC
    """
    def get_keys(self) -> tuple:
        raw_key = generate_eth_key()
        private_key = raw_key.to_hex()
        public_key = raw_key.public_key.to_hex()
        return public_key, private_key

    def crypt(self, message: str, key: str) -> bytes:
        return encrypt(key, message)

    def decrypt(self, cmessage: bytes, key: str) -> str:
        return decrypt(key, cmessage)
