from typing import Optional

from bunnet import Document, Link

from app.models.user import User


class Character(Document):
    name: str
    char_class: str
    race: str
    level: int
    user: Optional[Link[User]] = None

    class Settings:
        name = "characters"
