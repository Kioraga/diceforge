from flask import flash, redirect, url_for
from flask_login import LoginManager

from db import srp
import models.userdto as UserDto

lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    return UserDto.find(srp, user_id)


@lm.unauthorized_handler
def unauthorized_handler():
    flash("Unauthorized")
    return redirect(url_for("home.index"))