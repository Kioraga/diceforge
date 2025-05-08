from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager
import sirope
from datetime import datetime

from views import blueprints
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
    lm.login_view = "auth.login"

    # Registrando los blueprints
    for bp in blueprints:
        app.register_blueprint(bp)

    app.register_error_handler(404, lambda e: render_template("errors/404.html"))

    return app, lm, srp


app, lm, srp = create_app()


@lm.user_loader
def user_loader(username):
    return UserDto(srp, username)


@lm.unauthorized_handler
def unauthorized_handler():
    flash("Unauthorized")
    return redirect(url_for("home.index"))


if __name__ == "__main__":
    app.run(debug=True)
