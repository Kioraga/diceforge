from flask import Blueprint, session, jsonify


def get_blueprint():
    themes = Blueprint("themes", __name__)
    return themes


themes_bp = get_blueprint()


@themes_bp.route('/set-theme/<theme>', methods=['POST'])
def set_theme(theme):
    """Establece el tema en la sesión"""
    # Validar que el tema es uno de los permitidos
    allowed_themes = ['mocha', 'latte']

    if theme in allowed_themes:
        print(f"Estableciendo tema: {theme}")
        session['theme'] = theme
        return jsonify({'success': True, 'theme': theme})
    else:
        return jsonify({'success': False, 'error': 'Tema no válido'}), 400


@themes_bp.route('/get-theme', methods=['GET'])
def get_theme():
    """Obtiene el tema actual de la sesión"""
    current_theme = session.get('theme', 'mocha')
    return jsonify({'theme': current_theme})