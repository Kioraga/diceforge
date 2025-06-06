from flask import Blueprint, session, jsonify
import app


def get_blueprint():
    themes = Blueprint("themes", __name__)
    return themes


themes_bp = get_blueprint()


@themes_bp.route('/set-theme/<string:theme>', methods=['POST'])
def set_theme(theme):
    session['theme'] = theme
    print("Tema actualizado:", theme)

    return jsonify({'success': True}), 200
