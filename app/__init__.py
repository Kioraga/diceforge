from datetime import datetime

from bunnet import init_bunnet
from flask import Flask, render_template, flash, redirect, url_for, session
from flask_login import LoginManager
from pymongo import MongoClient

import app.models as models
from app.plugins import plugin_manager
from app.utils import hashlib_md5

lm = LoginManager()


def create_app():
    # Flask app configuration
    app = Flask(__name__, instance_relative_config=True)

    app.name = "Diceforge"
    app.config.from_pyfile("config.py")
    app.jinja_env.globals["title"] = app.name
    app.jinja_env.filters["hashlib_md5"] = hashlib_md5
    app.jinja_env.globals.update(now=datetime.now)

    # Función para obtener el tema actual
    def get_current_theme():
        return session.get('theme', 'mocha')  # 'mocha' como tema por defecto

    # Hacer la función disponible en todas las plantillas
    app.jinja_env.globals['get_current_theme'] = get_current_theme

    # Login manager configuration
    lm.init_app(app)
    lm.login_view = "auth.login"

    # Database initialization
    try:
        client = MongoClient("mongodb://mongodb:27017", serverSelectionTimeoutMS=5000)
        init_bunnet(database=client.diceforge, document_models=models.__all__)
        print("Connection to MongoDB established successfully")
    except Exception as e:
        print("Failed to connect to MongoDB:", e)
        exit(1)

    # Plugin manager initialization
    plugin_manager.load_all_plugins()

    # Registering the blueprints
    from . import views

    app.register_blueprint(views.home_bp)
    app.register_blueprint(views.auth_bp)
    app.register_blueprint(views.account_bp)
    app.register_blueprint(views.characters_bp)
    app.register_blueprint(views.plugins_bp)
    app.register_blueprint(views.themes_bp)

    app.register_error_handler(404, lambda e: render_template("errors/404.html"))

    return app


@lm.user_loader
def load_user(username):
    return models.User.find_one(models.User.username == username).run()


@lm.unauthorized_handler
def unauthorized_handler():
    flash("Tienes que iniciar sesión para acceder a esta página.", "error")
    return redirect(url_for("auth.login"))
