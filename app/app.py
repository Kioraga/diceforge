from flask import Flask
from flask_login import LoginManager
import sirope
from datetime import datetime

from blueprints.main import main
from blueprints.auth import auth


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    lm = LoginManager()
    srp = sirope.Sirope()

    app.name = "Diceforge"
    app.jinja_env.globals["title"] = app.name
    app.jinja_env.globals.update(now=datetime.now)

    app.register_blueprint(main.main_bp)
    app.register_blueprint(auth.auth_bp)

    return app, lm, srp


app, lm, srp = create_app()


if __name__ == "__main__":
    app.run(debug=True)
