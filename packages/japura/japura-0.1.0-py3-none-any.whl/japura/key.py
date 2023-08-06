from cryptography.fernet import Fernet
from typing import Optional, Union

import bcrypt


class SecureKey:
    """The SecureKey class provides methods to generate and manage secure keys."""

    @staticmethod
    def fernet() -> bytes:
        """Generates a new Fernet key.

        Returns
        -------
        bytes
            A secure key generated using Fernet algorithm.
        """
        return Fernet.generate_key()

    @staticmethod
    def bcrypt(plain: str, hashed: Optional[bytes] = b"") -> Union[bool, bytes]:
        """Generates a bcrypt hash from a plaintext password or checks if a plaintext password matches a bcrypt hash.

        Parameters
        ----------
        plain : str
            The plaintext password to be hashed.
        hashed : Optional[bytes]
            The bcrypt hash to compare the plaintext password against. If not provided, a new hash will be generated.

        Returns
        -------
        Union[bool, bytes]
            If hashed is provided, returns True if the plaintext password matches the hash, False otherwise. 
            If hashed is not provided, returns a new bcrypt hash generated from the plaintext password.
        """
        if not hashed:
            return bcrypt.hashpw(plain.encode(), bcrypt.gensalt(rounds=13))
        return bcrypt.checkpw(plain.encode(), hashed)
