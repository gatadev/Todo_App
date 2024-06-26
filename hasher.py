from hashlib import sha256

from Database import Database

class Hasher:
    def __init__(self) -> None:
        self.db = Database()

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def verify_password(self, stored_password, provided_password):
        return stored_password == self.hash_password(provided_password)

    def store_user(self, username, password):
        hashed_password = self.hash_password(password)
        self.db.add_user(username, hashed_password)

    def check_user(self, username, password) -> bool:
        user = self.db.get_user(username)
        if user:
            stored_username, stored_password = user[1], user[2]
            if stored_username == username:
                return self.verify_password(stored_password, password)
        return False