from typing import Optional

from bunnet import Document, Link

from app.models.user import User


class Character(Document):
    name: str
    race: str
    char_class: str
    level: int
    ability_scores: dict[str, int]
    background: Optional[dict[str, str]] = None
    info: Optional[dict[str, str]] = None
    spells: Optional[dict[str, str]] = None
    user: Optional[Link[User]] = None

    class Settings:
        name = "characters"
