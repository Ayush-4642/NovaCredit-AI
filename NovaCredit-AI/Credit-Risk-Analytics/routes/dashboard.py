from flask import Blueprint, render_template

from database.database import get_summary_stats, get_chart_data

dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/dashboard")
def dashboard():
    """Customer Statistics Page — age/loan/income/credit-score stats."""
    stats = get_summary_stats()
    charts = get_chart_data()
    return render_template("dashboard.html", stats=stats, charts=charts)
