from flask_login import UserMixin
import werkzeug.security as safe
from bunnet import Document


class User(Document, UserMixin):
    username: str
    email: str
    password: str

    class Settings:
        name = "users"

    def get_id(self):
        return self.username

    @staticmethod
    def hash_password(password: str) -> str:
        return safe.generate_password_hash(password)

    def chk_password(self, password) -> bool:
        return safe.check_password_hash(self.password, password)
