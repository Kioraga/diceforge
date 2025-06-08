from flask import Blueprint, render_template, request, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from pydantic import ValidationError

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
    characters = Character.find(
        Character.user.id == current_user.id,
        fetch_links=True
    ).to_list()

    return render_template("characters/character_gallery.html", characters=characters, compendium=compendium)


@characters_bp.route("/characters/create")
@login_required
def create_character():
    races = compendium.race_names()
    classes = compendium.class_names()

    return render_template("characters/character_creator.html", races=races, classes=classes)


@characters_bp.route("/characters/create", methods=["POST"])
@login_required
def create_character_post():
    character = Character(user=current_user,
                          name=request.form["name"],
                          race=compendium.get_race_id(request.form["race"]),
                          char_class=compendium.get_class_id(request.form["class"]),
                          level=1,
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
                          })

    character.update_ability_modifiers()
    character.hp = compendium.get_class_hp(character.char_class) + character.ability_modifiers.get('constitution', 0)
    character.update_dependencies()

    character.update()
    flash("Se ha creado el personaje correctamente.", "success")

    return redirect(url_for("characters.character_gallery"))


@characters_bp.route("/characters/<char_id>")
@login_required
def character_detail(char_id):
    try:
        character = Character.get(char_id, fetch_links=True).run()

        if character.user.id != current_user.id:
            flash("No tienes permiso para ver este personaje.", "error")
            return redirect(url_for("characters.character_gallery"))

        if character.check_dependencies() is False or character is None:
            flash("No se ha podido cargar el personaje.", "error")
            return redirect(url_for("characters.character_gallery"))

        response = make_response(
            render_template("characters/character.html", character=character, compendium=compendium))
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    except ValidationError:
        flash("ID de personaje inválido.", "error")
        return redirect(url_for("characters.character_gallery"))


@characters_bp.route("/update_character/<char_id>", methods=["POST"])
@login_required
def update_character(char_id):
    character = Character.get(char_id).run()
    if not character:
        flash("Personaje no encontrado.", "error")
        return redirect(url_for("characters.character_gallery"))

    try:
        def select_modal(modal):
            switch = {
                "base": update_base,
                "stats": update_stats,
                "saving_throws": update_saving_throws,
                "skills": update_skills,
            }
            switch.get(modal)()

        def update_base():
            character.name = request.form.get('name')
            character.race = compendium.get_race_id(request.form.get('race'))
            character.char_class = compendium.get_class_id(request.form.get('char_class'))
            character.level = int(request.form.get('level'))
            character.hp = int(request.form.get('hp'))

        def update_stats():
            character.ability_scores = {
                "strength": int(request.form.get('strength')),
                "dexterity": int(request.form.get('dexterity')),
                "constitution": int(request.form.get('constitution')),
                "intelligence": int(request.form.get('intelligence')),
                "wisdom": int(request.form.get('wisdom')),
                "charisma": int(request.form.get('charisma')),
            }

        def update_saving_throws():
            abilities = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]
            character.proficiencies = {
                ability: {
                    "proficiency": request.form.get(f'{ability}_proficiency') == 'on'
                } for ability in abilities
            }

        def update_skills():
            skills = [
                "acrobatics", "arcana", "athletics", "deception", "history",
                "performance", "intimidation", "investigation", "sleight_of_hand",
                "stealth", "survival", "perception", "persuasion", "insight",
                "medicine", "nature", "religion", "animal_handling"
            ]
            character.proficiencies = {
                skill: {
                    "proficiency": request.form.get(f'{skill}_proficiency') == 'on',
                    "expertise": request.form.get(f'{skill}_expertise') == 'on'
                } for skill in skills
            }

        select_modal(request.form.get('modal'))

        character.save()

        flash("Personaje actualizado correctamente.", "success")
        return redirect(url_for("characters.character_detail", char_id=char_id))

    except Exception as e:
        flash(f"Error al actualizar el personaje: {str(e)}", "error")
        return redirect(url_for("characters.character_detail", char_id=char_id))


@characters_bp.route("/delete_character/<char_id>", methods=["POST"])
@login_required
def delete_character(char_id):
    character = Character.get(char_id).run()
    if not character:
        flash("Personaje no encontrado.", "error")
        return redirect(url_for("characters.character_gallery"))

    character.delete()
    flash("Personaje eliminado correctamente.", "success")
    return redirect(url_for("characters.character_gallery"))
