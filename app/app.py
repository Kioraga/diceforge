from flask import Flask
from flask_login import LoginManager
import sirope
from blueprints.main import main


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    lm = LoginManager()
    srp = sirope.Sirope()

    app.register_blueprint(main.main_bp, url_prefix="/")

    return app, lm, srp


app, lm, srp = create_app()


if __name__ == "__main__":
    app.run(debug=True)
