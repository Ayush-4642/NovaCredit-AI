import os
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, flash, send_file

from config import Config
from database.database import insert_prediction, get_prediction_by_id
from models.predictor import predict_risk

predict_bp = Blueprint("predict", __name__)

REQUIRED_FIELDS = [
    "customer_name", "age", "gender", "marital_status", "city",
    "education_level", "employment_status", "income", "credit_score",
    "years_employed", "loan_amount", "loan_term", "existing_debt",
    "previous_loans", "late_payments", "monthly_expenses",
    "savings_balance", "debt_to_income_ratio", "loan_purpose",
]

NUMERIC_FIELDS = {
    "age": (18, 100), "income": (0, None), "credit_score": (300, 900),
    "years_employed": (0, 60), "loan_amount": (0, None), "loan_term": (1, 480),
    "existing_debt": (0, None), "previous_loans": (0, 50),
    "late_payments": (0, 100), "monthly_expenses": (0, None),
    "savings_balance": (0, None), "debt_to_income_ratio": (0, 50),
}


def validate_form(form):
    """Server-side validation mirroring the client-side rules."""
    errors = {}
    for field in REQUIRED_FIELDS:
        value = form.get(field, "").strip()
        if not value:
            errors[field] = "This field is required."

    for field, (min_val, max_val) in NUMERIC_FIELDS.items():
        value = form.get(field, "").strip()
        if not value:
            continue
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                errors[field] = f"Must be at least {min_val}."
            if max_val is not None and num > max_val:
                errors[field] = f"Must be at most {max_val}."
        except ValueError:
            errors[field] = "Must be a valid number."

    return errors


@predict_bp.route("/predict", methods=["GET", "POST"])
def predict():
    if request.method == "GET":
        return render_template("predict.html")

    form = request.form
    errors = validate_form(form)

    if errors:
        return render_template("predict.html", errors=errors, form_data=form.to_dict())

    try:
        result = predict_risk(form)

        record = form.to_dict()
        record["prediction"] = result["prediction"]
        record["prediction_probability"] = result["probability"]

        record_id = insert_prediction(record)
    except Exception as exc:
        flash(f"Could not generate a prediction: {exc}", "error")
        return render_template("predict.html", form_data=form.to_dict())

    return redirect(url_for("predict.result", record_id=record_id))


@predict_bp.route("/predict/result/<int:record_id>")
def result(record_id):
    record = get_prediction_by_id(record_id)
    if not record:
        flash("Prediction record not found.", "error")
        return redirect(url_for("predict.predict"))

    reasons, tips = [], []
    from models.predictor import generate_recommendation
    reasons, tips = generate_recommendation(record["prediction"], record)

    return render_template("result.html", record=record, reasons=reasons, tips=tips)


@predict_bp.route("/predict/report/view/<int:record_id>")
def view_report(record_id):
    record = get_prediction_by_id(record_id)
    if not record:
        flash("Prediction record not found.", "error")
        return redirect(url_for("history.history"))

    from models.predictor import generate_recommendation
    reasons, tips = generate_recommendation(record["prediction"], record)
    return render_template("report.html", record=record, reasons=reasons, tips=tips)


@predict_bp.route("/predict/report/<int:record_id>")
def download_report(record_id):

    record = get_prediction_by_id(record_id)
    if not record:
        flash("Prediction record not found.", "error")
        return redirect(url_for("history.history"))

    from models.predictor import generate_recommendation
    reasons, tips = generate_recommendation(record["prediction"], record)

    from utils.pdf_report import build_prediction_pdf
    filename = f"credit_risk_report_{record_id}.pdf"
    filepath = os.path.join(Config.REPORTS_DIR, filename)
    build_prediction_pdf(record, reasons, tips, filepath)

    return send_file(filepath, as_attachment=True, download_name=filename)
