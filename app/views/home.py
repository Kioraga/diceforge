from flask import Blueprint, render_template


def get_blueprint():
    home = Blueprint(
        "home", __name__, template_folder="templates", static_folder="static"
    )

    return home


home_bp = get_blueprint()


@home_bp.route("/")
def index():
    return render_template("home/index.html")
