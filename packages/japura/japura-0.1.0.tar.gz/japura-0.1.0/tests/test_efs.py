from japura.efs import SecureFile
from japura.key import SecureKey

import os


def test_encrypt_decrypt():
    filename = "test_secure_file.txt"

    key = SecureKey.fernet()

    with open(filename, 'w') as f:
        f.write("This is a test file.")

    sf = SecureFile(filename, key)
    sf.encrypt()
    assert os.path.getsize(filename) > 0
    assert sf.decrypt() == b"This is a test file."

    os.remove(filename)
