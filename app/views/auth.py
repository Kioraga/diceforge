from flask import Blueprint, request, render_template, redirect, url_for, flash
import flask_login

from app.models.user import User

import app


def get_blueprint():
    auth = Blueprint(
        "auth", __name__, template_folder="templates", static_folder="static"
    )
    lm = app.lm

    return auth, lm


auth_bp, lm = get_blueprint()


@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")


@auth_bp.route("/register")
def register():
    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["POST"])
def login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = request.form.get("remember")

    user = User.find_one(User.username == username).run()
    if user is None or not user.chk_password(password):
        flash(
            "Nombre de usuario o contraseña no válidos. Por favor, inténtelo de nuevo.",
            "error",
        )
        return render_template("auth/login.html")

    if remember:
        flask_login.login_user(user, remember=True)
    else:
        flask_login.login_user(user)

    return redirect(url_for("characters.character_gallery"))


@auth_bp.route("/register", methods=["POST"])
def register_post():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")
    print(username)

    if password != confirm_password:
        flash("Las contraseñas no coinciden. Por favor, inténtelo de nuevo.", "error")
        return render_template("auth/register.html")

    if User.find_one(User.username == username).run() is not None:
        flash("El nombre de usuario ya existe. Por favor, elija otro.", "error")
        return render_template("auth/register.html")

    new_user = User(username=username, email=email, password=User.hash_password(password))
    new_user.save()

    user = User.find_one(User.username == username).run()
    if user is None:
        flash("Registration failed. Please try again.", "error")
        return render_template("auth/register.html")

    flask_login.login_user(user)

    return redirect(url_for("characters.character_gallery"))


@auth_bp.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("home.index"))
