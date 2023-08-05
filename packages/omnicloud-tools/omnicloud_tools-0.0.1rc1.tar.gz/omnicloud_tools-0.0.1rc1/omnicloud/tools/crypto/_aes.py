# pylint: disable=missing-docstring

from os import environ as env
from base64 import b64encode as b64e, b64decode as b64d
from datetime import datetime as dt

from Crypto.Cipher import AES as Origin
from Crypto.Hash import SHA256
from Crypto import Random


class AES():
    '''
    Encrypt/decrypt data using the AES algorithm.

    Class requires a password. The password can be set in the environment variable SECRET_KEY.
    The argument "password" has priority over the environment variable.

    Args:
            key: A password for encryption/decryption
            block_size: Parameter for AES block size

    Raises:
        ValueError: If the argument "password" & the environment variable SECRET_KEY are empty
    '''

    def __init__(self, password: str | None = None, block_size: int | None = None):

        key_value = password or env.get('SECRET_KEY', None)
        if key_value is None:
            raise ValueError('Unknown encryption key!')

        self.key = SHA256.new(key_value.encode()).digest()
        self.block_size = block_size or Origin.block_size

    def encrypt(self, source: str | int | float | dict | dt) -> str:
        '''
        Encrypting data with AES algorithm.

        Args:
            source: The data for encrypt

        Returns:
            Encrypted data
        '''

        src = str(source).encode()

        padding = self.block_size - len(src) % self.block_size
        vector = Random.new().read(self.block_size)
        processor = Origin.new(self.key, Origin.MODE_CBC, vector)

        prepared = src + bytes([padding]) * padding
        data = vector + processor.encrypt(prepared)

        return b64e(data).decode("utf-8")

    def decrypt(self, source: str) -> str:
        '''
        Decrypt data using AES algorithm

        Args:
            source: Encrypted data as a string

        Raises:
            ValueError: If got an incorrect string

        Returns:
            Decrypted data as a string
        '''

        # pylint: disable=unsubscriptable-object

        src = b64d(source.encode("utf-8"))

        vector = src[:self.block_size]

        processor = Origin.new(self.key, Origin.MODE_CBC, vector)
        data = processor.decrypt(src[self.block_size:])
        padding = data[-1]

        if data[-padding:] != bytes([padding]) * padding:
            raise ValueError("Invalid padding...")

        return data[:-padding].decode()
