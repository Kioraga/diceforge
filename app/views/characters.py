from flask import Blueprint, render_template, url_for
from flask_login import login_required

from app.models import Character


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
        Character(name="Astarion", char_class="Rogue", race="High Elf", level=1),
        Character(name="Shadowheart", char_class="Cleric", race="Half-Elf", level=1),
        Character(name="Gale", char_class="Wizard", race="Human", level=1),
        Character(name="Lae'zel", char_class="Fighter", race="Githyanki", level=1),
        Character(name="Wyll", char_class="Warlock", race="Human", level=1),
        Character(name="Karlach", char_class="Barbarian", race="Tiefling", level=1),
        Character(name="Halsin", char_class="Druid", race="Wood Elf", level=5),
        Character(name="Minthara", char_class="Paladin", race="Drow", level=5),
        Character(name="Jaheira", char_class="Druid", race="Half-Elf", level=7),
        Character(name="Minsc", char_class="Ranger", race="Human", level=7)
    ]

    return render_template("characters/character_gallery.html", characters=characters)


@characters_bp.route("/characters/create")
@login_required
def create_character():
    return render_template("characters/character_creator.html")


@characters_bp.route("/characters/<char_id>")
@login_required
def character_detail(char_id):
    character = Character(name="Astarion", char_class="Rogue", race="High Elf", level=1)

    return render_template("characters/character.html", character=character)
