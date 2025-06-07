from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from pydantic import ValidationError

from app.models import Character, User
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
    characters = Character.find(
        Character.user.id == current_user.id,
        fetch_links=True
    ).to_list()

    return render_template("characters/character_gallery.html", characters=characters)


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
                          hp=42,
                          ability_scores={
                              "strength": request.form.get("strength"),
                              "dexterity": request.form.get("dexterity"),
                              "constitution": request.form.get("constitution"),
                              "intelligence": request.form.get("intelligence"),
                              "wisdom": request.form.get("wisdom"),
                              "charisma": request.form.get("charisma"),
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

    character.ability_modifiers = calculate_ability_modifiers(character.ability_scores)

    character.save()
    flash("Se ha creado el personaje correctamente.", "success")

    return redirect(url_for("characters.character_gallery"))


@characters_bp.route("/characters/<char_id>")
@login_required
def character_detail(char_id):
    try:
        character = Character.get(char_id).run()

        if character is None:
            flash("No se ha podido cargar el personaje.", "error")
            return redirect(url_for("characters.character_gallery"))

        return render_template("characters/character.html", character=character)

    except ValidationError:
        flash("ID de personaje inválido.", "error")
        return redirect(url_for("characters.character_gallery"))


def calculate_ability_modifiers(ability_scores):
    modifiers = {}
    for ability, score in ability_scores.items():
        if score is not None:
            modifiers[ability] = (score - 10) // 2
        else:
            modifiers[ability] = None
    return modifiers
