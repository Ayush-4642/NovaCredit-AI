from flask import Blueprint, render_template

from database.database import get_summary_stats

home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    stats = get_summary_stats()
    return render_template("home.html", stats=stats)


@home_bp.route("/about")
def about():
    return render_template("about.html")
