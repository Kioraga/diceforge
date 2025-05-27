from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager
from datetime import datetime
from pymongo import MongoClient
from bunnet import init_bunnet

from app.plugins import plugin_manager, compendium
from app.utils import hashlib_md5
import app.models as models

lm = LoginManager()


def create_app():
    # Flask app configuration
    app = Flask(__name__, instance_relative_config=True)

    app.name = "Diceforge"
    app.debug = True
    app.config.from_pyfile("config.py")
    app.jinja_env.globals["title"] = app.name
    app.jinja_env.filters["hashlib_md5"] = hashlib_md5
    app.jinja_env.globals.update(now=datetime.now)

    # Login manager configuration
    lm.init_app(app)
    lm.login_view = "auth.login"

    # Database initialization
    try:
        client = MongoClient("mongodb://localhost:27017", serverSelectionTimeoutMS=5000)
        init_bunnet(database=client.diceforge, document_models=models.__all__)
        print("Connection to MongoDB established successfully")
    except Exception as e:
        print("Failed to connect to MongoDB:", e)
        exit(1)

    # Plugin manager initialization
    plugin_manager.load_all_plugins()
    print(compendium.get_races().keys())

    # Registering the blueprints
    from . import views

    app.register_blueprint(views.home_bp)
    app.register_blueprint(views.auth_bp)
    app.register_blueprint(views.account_bp)
    app.register_blueprint(views.characters_bp)

    app.register_error_handler(404, lambda e: render_template("errors/404.html"))

    return app


@lm.user_loader
def load_user(username):
    return models.User.find_one(models.User.username == username).run()


@lm.unauthorized_handler
def unauthorized_handler():
    flash("Tienes que iniciar sesión para acceder a esta página.", "error")
    return redirect(url_for("auth.login"))
