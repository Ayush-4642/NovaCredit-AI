from flask import Blueprint, render_template, jsonify

from database.database import get_chart_data, get_summary_stats
from models.predictor import load_artifacts
from config import Config

analytics_bp = Blueprint("analytics", __name__)


@analytics_bp.route("/analytics")
def analytics():
    stats = get_summary_stats()
    charts = get_chart_data()
    return render_template("analytics.html", stats=stats, charts=charts)


@analytics_bp.route("/api/analytics/data")
def analytics_data():
    """JSON endpoint consumed by static/js/charts.js."""
    charts = get_chart_data()
    return jsonify(charts)


@analytics_bp.route("/api/analytics/feature-importance")
def feature_importance():
    model, _ = load_artifacts()
    importances = list(zip(Config.MODEL_FEATURES, model.feature_importances_.tolist()))
    importances.sort(key=lambda x: x[1], reverse=True)
    return jsonify({
        "labels": [i[0] for i in importances],
        "values": [round(i[1], 4) for i in importances],
    })
