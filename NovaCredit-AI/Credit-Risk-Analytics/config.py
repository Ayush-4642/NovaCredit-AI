"""
Application configuration for the NovaCredit AI.
"""

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "credit-risk-analytics-secret-key")

    # Paths
    DATABASE_PATH = os.path.join(BASE_DIR, "database", "banking.db")
    MODEL_PATH = os.path.join(BASE_DIR, "random_forest_model.pkl")
    SCALER_PATH = os.path.join(BASE_DIR, "scaler.pkl")
    REPORTS_DIR = os.path.join(BASE_DIR, "reports")
    EXPORTS_DIR = os.path.join(BASE_DIR, "exports")

    # Pagination
    RECORDS_PER_PAGE = 10

    # Model feature order — MUST match the order used during training
    # in Model_Training.ipynb. Do not change this order.
    MODEL_FEATURES = [
        "age",
        "income",
        "credit_score",
        "existing_debt",
        "late_payments",
        "loan_amount",
        "savings_balance",
        "debt_to_income_ratio",
    ]
