from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

from app.models.user import User


def get_blueprint():
    account = Blueprint(
        "account", __name__, template_folder="templates", static_folder="static"
    )
    return account


account_bp = get_blueprint()


@account_bp.route("/profile")
@login_required
def profile():
    return render_template("account/profile.html")


@account_bp.route("/profile", methods=["POST"])
@login_required
def edit_account():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("Las contraseñas no coinciden. Por favor, inténtelo de nuevo.", "error")
        return render_template("account/profile.html")

    if username != current_user.username:
        if User.find_one(User.username == username).run() is not None:
            flash("El nombre de usuario ya existe. Por favor, elija otro.", "error")
            return render_template("account/profile.html")

    current_user.username = username
    current_user.email = email
    if password:
        current_user.password = generate_password_hash(password)

    current_user.save()
    flash("Perfil actualizado correctamente.", "success")

    return redirect(url_for("account.profile"))
