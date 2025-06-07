from typing import Optional

from bunnet import Document, Link

from app.models.user import User
from app.plugins import plugin_manager


class Character(Document):
    user: Link[User]
    name: str
    race: str
    char_class: str
    level: int
    hp: int
    ability_scores: dict[str, int]
    ability_modifiers: Optional[dict[str, int]] = {}
    proficiencies: Optional[dict[str, str]] = {}  # proficiency | expertise
    background: Optional[dict[str, str]] = {}
    info: Optional[dict[str, str]] = {}
    spells: Optional[dict[str, str]] = {}
    dependencies: Optional[list[str]] = []

    class Settings:
        name = "characters"

    def update_ability_modifiers(self):
        # Calcula los modificadores de habilidad basados en los valores de habilidad
        for ability, score in self.ability_scores.items():
            self.ability_modifiers[ability] = (score - 10) // 2

    def update_dependencies(self):
        # Actualiza las dependencias del personaje con los plugins habilitados
        self.dependencies = [plugin.id for plugin in plugin_manager.get_enabled_plugins()]

    def check_dependencies(self) -> bool:
        """Verifica si todas las dependencias del personaje están satisfechas."""
        for dependency in self.dependencies:
            plugin = plugin_manager.get_plugin(dependency)
            if plugin is None or not plugin.enabled:
                return False

        return True
