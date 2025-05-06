from flask import Blueprint, render_template


def get_blueprint():
    main = Blueprint(
        "main", __name__, template_folder="templates", static_folder="static"
    )

    return main


main_bp = get_blueprint()


@main_bp.route("/")
def index():
    return render_template("index.html")
