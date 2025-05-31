from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required

from app.plugins import plugin_manager, compendium


def get_blueprint():
    plugins = Blueprint(
        "plugins", __name__, template_folder="templates", static_folder="static"
    )

    return plugins


plugins_bp = get_blueprint()


@plugins_bp.route("/plugins")
@login_required
def plugin_list():
    plugins = plugin_manager.list_plugins()

    return render_template("plugins/plugin_manager.html", plugins=plugins, compendium=compendium)


@plugins_bp.route("/plugins/reload")
@login_required
def reload_plugins():
    plugin_manager.reload_plugins()
    flash("Se recargaron los plugins correctamente.", "success")

    return redirect(url_for("plugins.plugin_list"))


@plugins_bp.route("/plugins/<plugin_id>/enable")
@login_required
def enable_plugin(plugin_id):
    plugin_manager.enable_plugin(plugin_id)
    return redirect(url_for("plugins.plugin_list"))


@plugins_bp.route("/plugins/<plugin_id>/disable")
@login_required
def disable_plugin(plugin_id):
    plugin_manager.disable_plugin(plugin_id)
    return redirect(url_for("plugins.plugin_list"))
