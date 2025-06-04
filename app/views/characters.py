from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.models import Character
from app.plugins import compendium


def get_blueprint():
    characters = Blueprint(
        "characters", __name__, template_folder="templates", static_folder="static"
    )
    return characters


characters_bp = get_blueprint()


@characters_bp.route("/characters")
@login_required
def character_gallery():
    characters_test = [
        Character(name="Astarion", char_class="Rogue", race="High Elf", level=1, ability_scores={}),
        Character(name="Shadowheart", char_class="Cleric", race="Half-Elf", level=1, ability_scores={}),
        Character(name="Gale", char_class="Wizard", race="Human", level=1, ability_scores={}),
        Character(name="Lae'zel", char_class="Fighter", race="Githyanki", level=1, ability_scores={}),
        Character(name="Wyll", char_class="Warlock", race="Human", level=1, ability_scores={}),
        Character(name="Karlach", char_class="Barbarian", race="Tiefling", level=1, ability_scores={}),
        Character(name="Halsin", char_class="Druid", race="Wood Elf", level=5, ability_scores={}),
        Character(name="Minthara", char_class="Paladin", race="Drow", level=5, ability_scores={}),
        Character(name="Jaheira", char_class="Druid", race="Half-Elf", level=7, ability_scores={}),
        Character(name="Minsc", char_class="Ranger", race="Human", level=7, ability_scores={})
    ]

    return render_template("characters/character_gallery.html", characters=characters_test)


@characters_bp.route("/characters/create")
@login_required
def create_character():
    races = compendium.race_names()
    classes = compendium.class_names()

    return render_template("characters/character_creator.html", races=races, classes=classes)


@characters_bp.route("/characters/create", methods=["POST"])
@login_required
def create_character_post():
    character = Character(name=request.form["name"],
                          race=request.form["race"],
                          char_class=request.form["class"],
                          level=1,
                          ability_scores={
                              "strength": request.form.get("strength"),
                              "dexterity": request.form.get("dexterity"),
                              "constitution": request.form.get("constitution"),
                              "intelligence": request.form.get("intelligence"),
                              "wisdom": request.form.get("wisdom"),
                              "charisma": request.form.get("charisma")
                          },
                          background={
                              "name": request.form.get("bg_name", ""),
                              "features": request.form.get("bg_features", ""),
                              "ideals": request.form.get("bg_ideals", ""),
                              "bonds": request.form.get("bg_bonds", ""),
                              "flaws": request.form.get("bg_flaws", "")
                          },
                          info={
                              "alignment": request.form.get("alignment", ""),
                              "appearance": request.form.get("appearance", ""),
                              "history": request.form.get("history", "")
                          },
                          user=current_user)

    print(character)
    # character.save()

    flash("Se ha creado el personaje correctamente.", "success")

    return redirect(url_for("characters.character_gallery"))


@characters_bp.route("/characters/<char_id>")
@login_required
def character_detail(char_id):
    if char_id is None:
        character = Character(name="Astarion", char_class="Rogue", race="High Elf", level=1, ability_scores={})

    return render_template("characters/character.html", character=character)
