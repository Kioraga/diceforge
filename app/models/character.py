from typing import Optional

from bunnet import Document, Link

from app.models.user import User


class Character(Document):
    name: str
    race: str
    char_class: str
    level: int
    hp: int
    ability_scores: dict[str, int]
    ability_modifiers: Optional[dict[str, int]] = {}
    proficiencies: Optional[dict[str, str]] = {} # proficiency | expertise
    background: Optional[dict[str, str]] = {}
    info: Optional[dict[str, str]] = {}
    spells: Optional[dict[str, str]] = {}
    user: Optional[Link[User]] = None

    class Settings:
        name = "characters"

    def update_ability_modifiers(self):
        # Calcula los modificadores de habilidad basados en los valores de habilidad
        for ability, score in self.ability_scores.items():
            self.ability_modifiers[ability] = (score - 10) // 2