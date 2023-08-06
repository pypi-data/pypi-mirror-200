from cryptography.fernet import Fernet
from typing import Optional

import os


class SecureFile:
    """A class for encrypting and decrypting files using the Fernet encryption algorithm.

    Parameters
    ----------
    filename : str
        The name of the file to be encrypted or decrypted.
    key : bytes
        The encryption key used by Fernet algorithm.

    Methods
    -------
    encrypt(content: Optional[bytes]) -> None:
        Encrypts the content of the file using Fernet algorithm and the given encryption key.
    decrypt() -> bytes:
        Decrypts the content of the file using Fernet algorithm and the given encryption key.
    """

    def __init__(self, filename: str, key: bytes):
        """Constructs a SecureFile object with the given filename and encryption key.

        Parameters
        ----------
        filename : str
            The name of the file to be encrypted or decrypted.
        key : bytes
            The encryption key used by Fernet algorithm.
        """
        self.filename = filename
        self.key = key

    def encrypt(self, content: Optional[bytes] = None) -> None:
        """Encrypts the content of the file using Fernet algorithm and the given encryption key.

        Parameters
        ----------
        content : Optional[bytes]
            The content to be encrypted and written to the file. If None, the content of the file is encrypted.

        Raises
        ------
        EOFError
            If the file is empty, raises an EOFError with the message "File must contain content before attempting to read from it."
        """
        if os.path.getsize(self.filename) > 0:
            if not self.decrypt() or content:
                fernet = Fernet(self.key)
                with open(self.filename, 'rb+') as f:
                    data = fernet.encrypt(content or f.read())
                    f.seek(0)
                    f.write(data)
        else:
            raise EOFError("File must contain content before attempting to read from it.")

    def decrypt(self) -> bytes:
        """Decrypts the content of the file using Fernet algorithm and the given encryption key.

        Returns
        -------
        bytes
            The decrypted content if decryption is successful, otherwise returns None.
        """
        fernet = Fernet(self.key)
        with open(self.filename, 'rb') as f:
            data = None
            try:
                data = fernet.decrypt(f.read())
            except Exception:
                pass
        return data
