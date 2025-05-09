from flask import Blueprint, request, render_template, redirect, url_for, flash
import sirope

from models.userdto import UserDto


def get_blueprint():
    auth = Blueprint(
        "auth", __name__, template_folder="templates", static_folder="static"
    )
    srp = sirope.Sirope()

    return auth, srp


auth_bp, srp = get_blueprint()


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

    print(f"Username: {username}, Password: {password}")

    user = UserDto.find(srp, username)
    if user is None or not user.chk_password(password):
        flash("Invalid username or password. Please try again.", "error")
        return render_template("auth/login.html")

    return redirect(url_for("home.index"))


@auth_bp.route("/register", methods=["POST"])
def register_post():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    confirm_password = request.form.get("confirm_password")

    if password != confirm_password:
        flash("Passwords do not match. Please try again.", "error")
        return render_template("auth/register.html")

    if UserDto.find(srp, username) is not None:
        flash("Username already exists. Please choose a different one.", "error")
        return render_template("auth/register.html")

    print(f"Username: {username}, Email: {email}, Password: {password}")

    srp.save(UserDto(username, email, password))

    return redirect(url_for("home.index"))
