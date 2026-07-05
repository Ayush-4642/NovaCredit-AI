"""
Database layer for the NovaCredit AI.

Handles automatic creation of banking.db and the user_predictions table,
plus all CRUD/query helpers used by the routes.
"""

import sqlite3
from datetime import datetime

from config import Config


def get_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    """Create the database and table automatically if they do not exist."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS user_predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            customer_name TEXT,
            age INTEGER,
            gender TEXT,
            marital_status TEXT,
            city TEXT,
            education_level TEXT,
            employment_status TEXT,
            income REAL,
            credit_score INTEGER,
            years_employed INTEGER,
            loan_amount REAL,
            loan_term INTEGER,
            existing_debt REAL,
            previous_loans INTEGER,
            late_payments INTEGER,
            monthly_expenses REAL,
            savings_balance REAL,
            debt_to_income_ratio REAL,
            loan_purpose TEXT,
            prediction TEXT,
            prediction_probability REAL
        )
        """
    )
    conn.commit()
    conn.close()


def insert_prediction(data: dict) -> int:
    """Insert a new prediction record and return its id."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO user_predictions (
            timestamp, customer_name, age, gender, marital_status, city,
            education_level, employment_status, income, credit_score,
            years_employed, loan_amount, loan_term, existing_debt,
            previous_loans, late_payments, monthly_expenses, savings_balance,
            debt_to_income_ratio, loan_purpose, prediction, prediction_probability
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get("customer_name"),
            data.get("age"),
            data.get("gender"),
            data.get("marital_status"),
            data.get("city"),
            data.get("education_level"),
            data.get("employment_status"),
            data.get("income"),
            data.get("credit_score"),
            data.get("years_employed"),
            data.get("loan_amount"),
            data.get("loan_term"),
            data.get("existing_debt"),
            data.get("previous_loans"),
            data.get("late_payments"),
            data.get("monthly_expenses"),
            data.get("savings_balance"),
            data.get("debt_to_income_ratio"),
            data.get("loan_purpose"),
            data.get("prediction"),
            data.get("prediction_probability"),
        ),
    )
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_prediction_by_id(record_id: int):
    conn = get_connection()
    row = conn.execute(
        "SELECT * FROM user_predictions WHERE id = ?", (record_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def delete_prediction(record_id: int) -> bool:
    conn = get_connection()
    cursor = conn.execute("DELETE FROM user_predictions WHERE id = ?", (record_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def get_filtered_predictions(search="", risk_filter="all", sort_by="timestamp",
                              sort_dir="desc", page=1, per_page=10):
    """Return (records, total_count) applying search/filter/sort/pagination."""
    conn = get_connection()

    query = "SELECT * FROM user_predictions WHERE 1=1"
    count_query = "SELECT COUNT(*) FROM user_predictions WHERE 1=1"
    params = []

    if search:
        query += " AND (customer_name LIKE ? OR city LIKE ? OR loan_purpose LIKE ?)"
        count_query += " AND (customer_name LIKE ? OR city LIKE ? OR loan_purpose LIKE ?)"
        like = f"%{search}%"
        params.extend([like, like, like])

    if risk_filter in ("High Risk", "Low Risk"):
        query += " AND prediction = ?"
        count_query += " AND prediction = ?"
        params.append(risk_filter)

    total = conn.execute(count_query, params).fetchone()[0]

    allowed_sort_cols = {
        "timestamp", "customer_name", "age", "income", "credit_score",
        "loan_amount", "prediction_probability",
    }
    if sort_by not in allowed_sort_cols:
        sort_by = "timestamp"
    sort_dir = "ASC" if sort_dir.lower() == "asc" else "DESC"

    query += f" ORDER BY {sort_by} {sort_dir} LIMIT ? OFFSET ?"
    params.extend([per_page, (page - 1) * per_page])

    rows = conn.execute(query, params).fetchall()
    conn.close()
    return [dict(r) for r in rows], total


def get_all_predictions():
    conn = get_connection()
    rows = conn.execute(
        "SELECT * FROM user_predictions ORDER BY timestamp DESC"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_summary_stats():
    """Aggregate stats used across dashboard, analytics and admin pages."""
    conn = get_connection()
    total = conn.execute("SELECT COUNT(*) FROM user_predictions").fetchone()[0]

    high_risk = conn.execute(
        "SELECT COUNT(*) FROM user_predictions WHERE prediction = 'High Risk'"
    ).fetchone()[0]
    low_risk = conn.execute(
        "SELECT COUNT(*) FROM user_predictions WHERE prediction = 'Low Risk'"
    ).fetchone()[0]

    avg_row = conn.execute(
        """SELECT AVG(credit_score) AS avg_credit_score,
                  AVG(income) AS avg_income,
                  AVG(loan_amount) AS avg_loan_amount,
                  AVG(age) AS avg_age
           FROM user_predictions"""
    ).fetchone()

    conn.close()
    return {
        "total": total,
        "high_risk": high_risk,
        "low_risk": low_risk,
        "default_rate": round((high_risk / total) * 100, 2) if total else 0,
        "avg_credit_score": round(avg_row["avg_credit_score"] or 0, 1),
        "avg_income": round(avg_row["avg_income"] or 0, 2),
        "avg_loan_amount": round(avg_row["avg_loan_amount"] or 0, 2),
        "avg_age": round(avg_row["avg_age"] or 0, 1),
    }


def get_chart_data():
    """Return aggregated data used to feed the Chart.js analytics page."""
    conn = get_connection()

    def col(sql, params=()):
        return [dict(r) for r in conn.execute(sql, params).fetchall()]

    data = {
        "age_distribution": col(
            """SELECT
                CASE
                    WHEN age < 25 THEN '18-24'
                    WHEN age < 35 THEN '25-34'
                    WHEN age < 45 THEN '35-44'
                    WHEN age < 55 THEN '45-54'
                    ELSE '55+'
                END AS bucket, COUNT(*) AS count
               FROM user_predictions GROUP BY bucket"""
        ),
        "loan_purpose_distribution": col(
            "SELECT loan_purpose, COUNT(*) AS count FROM user_predictions "
            "GROUP BY loan_purpose"
        ),
        "prediction_distribution": col(
            "SELECT prediction, COUNT(*) AS count FROM user_predictions "
            "GROUP BY prediction"
        ),
        "city_wise": col(
            "SELECT city, COUNT(*) AS count FROM user_predictions "
            "GROUP BY city ORDER BY count DESC LIMIT 10"
        ),
        "monthly_trend": col(
            """SELECT strftime('%Y-%m', timestamp) AS month, COUNT(*) AS count
               FROM user_predictions GROUP BY month ORDER BY month"""
        ),
        "credit_score_distribution": col(
            """SELECT
                CASE
                    WHEN credit_score < 500 THEN 'Poor (<500)'
                    WHEN credit_score < 650 THEN 'Fair (500-649)'
                    WHEN credit_score < 750 THEN 'Good (650-749)'
                    ELSE 'Excellent (750+)'
                END AS bucket, COUNT(*) AS count
               FROM user_predictions GROUP BY bucket"""
        ),
        "income_distribution": col(
            """SELECT
                CASE
                    WHEN income < 300000 THEN '<3L'
                    WHEN income < 600000 THEN '3L-6L'
                    WHEN income < 1000000 THEN '6L-10L'
                    ELSE '10L+'
                END AS bucket, COUNT(*) AS count
               FROM user_predictions GROUP BY bucket"""
        ),
        "loan_distribution": col(
            """SELECT
                CASE
                    WHEN loan_amount < 200000 THEN '<2L'
                    WHEN loan_amount < 500000 THEN '2L-5L'
                    WHEN loan_amount < 1000000 THEN '5L-10L'
                    ELSE '10L+'
                END AS bucket, COUNT(*) AS count
               FROM user_predictions GROUP BY bucket"""
        ),
    }
    conn.close()
    return data
