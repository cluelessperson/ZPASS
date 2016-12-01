import os, io, sqlite3, base64, sys
import zpass.configuration as config

from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Storage():
    def __init__(self, file, passphrase):
        self.file = file
        self.sql = sqlite3.connect(':memory:')

        if not self._open(passphrase):
            print('creating')
            self._create(passphrase)
        self.sql.commit()


    def _open(self, passphrase):
        if os.path.isfile(self.file):
            with open(self.file, 'r') as f:
                self.salt = f.read(16)
                encrypted_database = f.read()
            self.key, _ = self.generate_key(passphrase, self.salt)

            decrypted_database = self.decrypt(encrypted_database, self.key)
            self.sql.cursor().executescript(decrypted_database)
            return True
        return False


    def _create(self, passphrase):
        self.key, self.salt = self.generate_key(passphrase)
        s = "CREATE TABLE IF NOT EXISTS credentials('id' INTEGER PRIMARY KEY, '%s' TEXT)" % ("' TEXT, '".join(config.headers))
        self.sql.execute(s)


    def _save(self, file):
        i = io.StringIO()
        for line in self.sql.iterdump():
            i.write( line + '\n' )

        decrypted_database = i.getvalue()
        encrypted_database = self.encrypt(decrypted_database, self.key)

        with open(file, 'wb') as f:
            f.write(self.salt)
            f.write(encrypted_database)

    @staticmethod
    def generate_key(passphrase, salt=None, iterations=500000):
        if salt is None:
            salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA512(),
            length=32,
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(passphrase))
        return key, salt

    @staticmethod
    def encrypt(raw_bytes, key):
        return Fernet(key).encrypt(raw_bytes)

    @staticmethod
    def decrypt(raw_bytes, key):
        try:
            return Fernet(key).decrypt(token)
        except InvalidToken:
            print('Wrong password')
            sys.exit(0)