from japura.key import SecureKey


class TestSecureKey:

    def test_fernet(self):
        key = SecureKey.fernet()
        assert isinstance(key, bytes)

    def test_bcrypt_hashing(self):
        password = "my_password"
        hashed_password = SecureKey.bcrypt(password)
        assert isinstance(hashed_password, bytes)

    def test_bcrypt_validation(self):
        password = "my_password"
        hashed_password = SecureKey.bcrypt(password)
        assert SecureKey.bcrypt(password, hashed_password)

    def test_bcrypt_validation_wrong_password(self):
        password = "my_password"
        wrong_password = "wrong_password"
        hashed_password = SecureKey.bcrypt(password)
        assert not SecureKey.bcrypt(wrong_password, hashed_password)
