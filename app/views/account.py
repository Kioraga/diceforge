from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash


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
