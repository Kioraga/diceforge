from flask import Blueprint, render_template
from flask_login import login_required

from app.models import CharacterDto


def get_blueprint():
    characters = Blueprint(
        "characters", __name__, template_folder="templates", static_folder="static"
    )
    return characters


characters_bp = get_blueprint()


@characters_bp.route("/characters")
@login_required
def character_gallery():
    characters = [
        CharacterDto("John Doe", "Fighter", 5),
        CharacterDto("Jane Smith", "Wizard", 3),
        CharacterDto("Bob Johnson", "Rogue", 4),
        CharacterDto("Alice Brown", "Cleric", 2),
        CharacterDto("Charlie White", "Paladin", 6),
        CharacterDto("Diana Green", "Ranger", 4),
        CharacterDto("Eve Black", "Sorcerer", 5),
        CharacterDto("Frank Blue", "Bard", 3),
        CharacterDto("Grace Yellow", "Monk", 2),
        CharacterDto("Hank Red", "Warlock", 4),
    ]

    return render_template("characters/character_gallery.html", characters=characters)
