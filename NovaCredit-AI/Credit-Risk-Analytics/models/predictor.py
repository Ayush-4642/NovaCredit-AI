"""
Prediction service wrapping the ALREADY TRAINED artifacts:

    random_forest_model.pkl
    scaler.pkl

No training happens here. This module only loads the artifacts and
runs inference, exactly reproducing the preprocessing used in
Model_Training.ipynb.

IMPORTANT — matches the training notebook exactly:
The Random Forest model in Model_Training.ipynb was fit directly on the
RAW (unscaled) feature values:

    rf.fit(X_train, y_train)          # <- unscaled

The StandardScaler in that notebook was fit separately and only used
for the KNN / MLP experiments, never for the Random Forest. Therefore
this service feeds RAW feature values into random_forest_model.pkl.
The scaler is still loaded and exposed (get_scaler) for transparency /
future use, but it is intentionally NOT applied before the Random
Forest prediction, since doing so would feed the model data on a
different scale than it was trained on and silently corrupt every
prediction.
"""

import joblib
import numpy as np
import pandas as pd

from config import Config


_model = None
_scaler = None


def load_artifacts():
    """Load the pkl artifacts once (lazy singleton)."""
    global _model, _scaler
    if _model is None:
        _model = joblib.load(Config.MODEL_PATH)
    if _scaler is None:
        _scaler = joblib.load(Config.SCALER_PATH)
    return _model, _scaler


def get_scaler():
    _, scaler = load_artifacts()
    return scaler


def build_feature_vector(form_data: dict) -> "pd.DataFrame":
    """Builds the feature vector in the EXACT order/column-names used during training."""
    values = {feature: [float(form_data[feature])] for feature in Config.MODEL_FEATURES}
    return pd.DataFrame(values, columns=Config.MODEL_FEATURES)


def generate_recommendation(prediction: str, form_data: dict):
    """Business-rule recommendation engine based on the applicant profile."""
    reasons = []
    tips = []

    credit_score = float(form_data.get("credit_score", 0))
    existing_debt = float(form_data.get("existing_debt", 0))
    dti = float(form_data.get("debt_to_income_ratio", 0))
    late_payments = float(form_data.get("late_payments", 0))
    savings = float(form_data.get("savings_balance", 0))
    income = float(form_data.get("income", 0))

    if prediction == "High Risk":
        if credit_score < 650:
            reasons.append("Low credit score")
            tips.append("Improve credit score before reapplying")
        if dti > 1.0:
            reasons.append("High debt-to-income ratio")
            tips.append("Reduce existing debt")
        if existing_debt > income:
            reasons.append("Existing debt exceeds annual income")
            tips.append("Pay down existing liabilities")
        if late_payments > 3:
            reasons.append("Frequent late payments")
            tips.append("Maintain a consistent on-time payment history")
        if savings < income * 0.1:
            reasons.append("Low savings relative to income")
            tips.append("Increase savings balance")
        if not reasons:
            reasons.append("Overall risk profile flagged by the model")
        tips.append("Apply again after improving the above factors")
    else:
        reasons.append("Healthy credit score and manageable debt levels")
        tips.append("Maintain current financial discipline")
        tips.append("Continue timely repayments to preserve loan eligibility")

    return reasons, tips


def predict_risk(form_data: dict):
    """
    Runs the full prediction flow:
      validate -> build feature vector -> predict with random_forest_model.pkl
      -> return label, probability, recommendation
    """
    model, _ = load_artifacts()

    features = build_feature_vector(form_data)
    proba = model.predict_proba(features)[0]

    # Class 1 == loan_default == High Risk (matches loan_default target)
    default_index = list(model.classes_).index(1) if 1 in model.classes_ else 1
    probability_of_default = float(proba[default_index])

    prediction_label = "High Risk" if probability_of_default >= 0.5 else "Low Risk"
    confidence = probability_of_default if prediction_label == "High Risk" else (1 - probability_of_default)

    reasons, tips = generate_recommendation(prediction_label, form_data)

    return {
        "prediction": prediction_label,
        "probability": round(probability_of_default * 100, 2),
        "confidence": round(confidence * 100, 2),
        "reasons": reasons,
        "tips": tips,
    }
