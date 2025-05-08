from flask import Flask
from flask import render_template, flash, redirect, url_for
from flask_login import LoginManager
import sirope
from datetime import datetime

from blueprints.main import main
from blueprints.auth import auth
from model.userdto import UserDto


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    lm = LoginManager()
    srp = sirope.Sirope()

    app.name = "Diceforge"
    app.config.from_pyfile("config.py")
    app.jinja_env.globals["title"] = app.name
    app.jinja_env.globals.update(now=datetime.now)

    lm.init_app(app)

    app.register_blueprint(main.main_bp)
    app.register_blueprint(auth.auth_bp)

    app.register_error_handler(404, lambda e: render_template("errors/404.html"))

    return app, lm, srp


app, lm, srp = create_app()


# Initialize the LoginManager
@lm.user_loader
def user_loader(username):
    return UserDto(srp, username)


@lm.unauthorized_handler
def unauthorized_handler():
    flash("Unauthorized")
    return redirect(url_for("main.index"))


if __name__ == "__main__":
    app.run(debug=True)
