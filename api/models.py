from dataclasses import dataclass
import os


@dataclass
class User():
    id: str
    name: str
    password: str
    email: str = "no email"
    _is_authenticated: bool = False

    def to_json(self):
        return {"name": self.name, "email": self.email}

    def is_authenticated(self):
        return self._is_authenticated

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)


def authenticate_user(user):
    credentials_correct = user.name == os.getenv("USER") and user.password == os.getenv("PASSWORD")
    if credentials_correct:
        user._is_authenticated = True
    return credentials_correct
