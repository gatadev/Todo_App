from hashlib import sha256

class Hasher:
    def __init__(self) -> None:
        pass

    def hash_password(self, password):
        return sha256(password.encode()).hexdigest()

    def verify_password(self, stored_password, provided_password):
        return stored_password == self.hash_password(provided_password)

    def store_user(self, username, password):
        with open('users.txt', 'a') as f:
            f.write(f"{username},{self.hash_password(password)}\n")

    def check_user(self, username, password) -> bool:
        try:
            with open('users.txt', 'r') as f:
                users = f.readlines()
                for user in users:
                    stored_username, stored_password = user.strip().split(',')
                    if stored_username == username:
                        return self.verify_password(stored_password, password)
        except FileNotFoundError:
            return False
        return False
