from flask import Blueprint, render_template


def get_blueprint():
    auth = Blueprint(
        "auth", __name__, template_folder="templates", static_folder="static"
    )

    return auth


auth_bp = get_blueprint()


@auth_bp.route("/login")
def login():
    return render_template("login.html")


@auth_bp.route("/register")
def register():
    return render_template("register.html")
