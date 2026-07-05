import csv
import os

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file, jsonify

from config import Config
from database.database import (
    get_filtered_predictions, delete_prediction, get_all_predictions,
)

history_bp = Blueprint("history", __name__)


@history_bp.route("/history")
def history():
    search = request.args.get("search", "").strip()
    risk_filter = request.args.get("risk", "all")
    sort_by = request.args.get("sort_by", "timestamp")
    sort_dir = request.args.get("sort_dir", "desc")
    page = max(int(request.args.get("page", 1)), 1)

    records, total = get_filtered_predictions(
        search=search, risk_filter=risk_filter, sort_by=sort_by,
        sort_dir=sort_dir, page=page, per_page=Config.RECORDS_PER_PAGE,
    )

    total_pages = max((total + Config.RECORDS_PER_PAGE - 1) // Config.RECORDS_PER_PAGE, 1)

    return render_template(
        "history.html", records=records, total=total, page=page,
        total_pages=total_pages, search=search, risk_filter=risk_filter,
        sort_by=sort_by, sort_dir=sort_dir,
    )


@history_bp.route("/history/delete/<int:record_id>", methods=["POST"])
def delete(record_id):
    success = delete_prediction(record_id)
    if success:
        flash("Record deleted successfully.", "success")
    else:
        flash("Record not found.", "error")
    return redirect(url_for("history.history"))


@history_bp.route("/history/export/csv")
def export_csv():
    records = get_all_predictions()
    filepath = os.path.join(Config.EXPORTS_DIR, "prediction_history.csv")

    if records:
        fieldnames = list(records[0].keys())
    else:
        fieldnames = ["id", "timestamp", "customer_name", "prediction"]

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return send_file(filepath, as_attachment=True, download_name="prediction_history.csv")


@history_bp.route("/history/export/pdf")
def export_pdf():
    records = get_all_predictions()
    from utils.pdf_report import build_history_pdf
    filepath = os.path.join(Config.EXPORTS_DIR, "prediction_history.pdf")
    build_history_pdf(records, filepath)
    return send_file(filepath, as_attachment=True, download_name="prediction_history.pdf")
