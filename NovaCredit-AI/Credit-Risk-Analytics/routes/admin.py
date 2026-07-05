from flask import Blueprint, render_template

from database.database import get_summary_stats, get_chart_data, get_all_predictions

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/admin")
def admin():
    stats = get_summary_stats()
    charts = get_chart_data()
    recent = get_all_predictions()[:8]
    return render_template("admin.html", stats=stats, charts=charts, recent=recent)
