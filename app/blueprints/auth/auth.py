from flask import Blueprint
from flask import request
from flask import render_template, redirect, url_for, flash


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


@auth_bp.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")

    print(f"Username: {username}, Password: {password}")

    return redirect(url_for("main.index"))


@auth_bp.route("/register", methods=["POST"])
def register_post():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("Passwords do not match. Please try again.", "error")
        return render_template("register.html")

    print(f"Username: {username}, Email: {email}, Password: {password}")

    return redirect(url_for("main.index"))
