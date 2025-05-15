from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager
import sirope
from datetime import datetime

from app.utils import hashlib_md5
from app.models.userdto import UserDto

lm = LoginManager()
srp = sirope.Sirope()


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.name = "Diceforge"
    app.config.from_pyfile("config.py")
    app.jinja_env.globals["title"] = app.name
    app.jinja_env.filters['hashlib_md5'] = hashlib_md5
    app.jinja_env.globals.update(now=datetime.now)

    lm.init_app(app)
    lm.login_view = "auth.login"

    from . import views

    app.register_blueprint(views.home_bp)
    app.register_blueprint(views.auth_bp)

    app.register_error_handler(404, lambda e: render_template("errors/404.html"))

    return app


@lm.user_loader
def load_user(user_id):
    return UserDto.find(srp, user_id)


@lm.unauthorized_handler
def unauthorized_handler():
    flash("Unauthorized")
    return redirect(url_for("home.index"))
