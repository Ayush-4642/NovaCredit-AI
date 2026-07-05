# NovaCredit AI

A portfolio-quality FinTech web application that wraps an existing, already-trained
Random Forest credit-risk model in a modern Flask + SQLite web app: enter applicant
data, get an instant risk prediction with explainable recommendations, browse full
history, and explore interactive analytics.

> This project does **not** retrain or modify any machine learning model. It builds
> the full-stack application around the artifacts produced in `EDA.ipynb` and
> `Model_Training.ipynb` — `random_forest_model.pkl` and `scaler.pkl`.

## ⚠️ Important note on the ML pipeline

`Model_Training.ipynb` trains the **Random Forest** classifier directly on the raw
(unscaled) feature values — `StandardScaler` in that notebook is only used for the
KNN and MLP experiments. To stay faithful to how the model was actually trained,
`models/predictor.py` feeds **raw** feature values into `random_forest_model.pkl`
and does **not** apply `scaler.pkl` before that prediction (applying it would put
the model's inputs on a completely different scale than it saw during training and
silently produce incorrect predictions). `scaler.pkl` is still loaded and exposed
in the codebase for transparency and any future model that needs it.

## Features

- 🎯 Multi-step loan risk prediction form with client + server-side validation
- 🧠 Explainable results: risk gauge, probability, plain-language risk factors and
  recommendations
- 🗂️ Full prediction history — search, sort, filter, paginate, delete
- 📄 Branded PDF report per prediction (ReportLab) + printable in-browser report
- 📊 Interactive Chart.js analytics: age/income/credit-score/loan distributions,
  city-wise counts, monthly trend, feature importance, risk split
- 📈 Customer statistics page and Admin dashboard with portfolio-wide KPIs
- ⬇️ Export prediction history to CSV or PDF
- 🌗 Dark / light mode toggle, remembered via `localStorage`
- 💎 Glassmorphism, gradient, animated FinTech UI — fully responsive

## Folder Structure

```
Credit-Risk-Analytics/
├── app.py                     # Flask app factory & entry point
├── config.py                  # Paths, feature order, pagination config
├── requirements.txt
├── README.md
├── random_forest_model.pkl    # Existing trained model (not modified)
├── scaler.pkl                 # Existing scaler (loaded, not applied to RF)
├── banking_risk_analytics_dataset.csv
├── EDA.ipynb
├── Model_Training.ipynb
│
├── database/
│   ├── database.py            # SQLite connection, schema, CRUD, aggregates
│   └── banking.db             # Auto-created on first run
│
├── models/
│   └── predictor.py           # Loads pkl artifacts, runs inference, recommendations
│
├── utils/
│   └── pdf_report.py          # ReportLab PDF generation (single + history reports)
│
├── routes/
│   ├── home.py                # Home + About
│   ├── predict.py             # Prediction form, result, PDF/report downloads
│   ├── analytics.py           # Analytics page + JSON chart data API
│   ├── dashboard.py           # Customer Statistics page
│   ├── history.py             # History table, search/filter/sort, exports, delete
│   └── admin.py                # Admin dashboard
│
├── templates/
│   ├── base.html, home.html, predict.html, result.html, history.html,
│   │   analytics.html, dashboard.html, admin.html, about.html, report.html
│
├── static/
│   ├── css/style.css          # Full design system (glassmorphism, dark/light)
│   └── js/script.js, charts.js
│
├── reports/                   # Generated single-prediction PDF reports
├── exports/                   # Generated CSV/PDF history exports
└── screenshots/               # Placeholder for README screenshots
```

## Installation

```bash
cd Credit-Risk-Analytics
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## How to Run

```bash
python app.py
```

The app starts on **http://localhost:5000**. `banking.db` and its
`user_predictions` table are created automatically on first run — no manual
setup required.

## Technologies Used

| Layer      | Technology                              |
|------------|------------------------------------------|
| Frontend   | HTML5, CSS3, JavaScript, Chart.js         |
| Backend    | Python, Flask                             |
| Database   | SQLite                                    |
| ML         | scikit-learn Random Forest (pre-trained)  |
| PDF        | ReportLab                                 |

## Screenshots

_Add screenshots of the Home, Prediction, Result, Analytics and Admin pages here._

- `screenshots/home.png`
- `screenshots/predict.png`
- `screenshots/result.png`
- `screenshots/analytics.png`
- `screenshots/admin.png`

## Future Improvements

- User authentication & role-based access (admin vs. loan officer)
- Model versioning and A/B testing between Random Forest / KNN / MLP
- SHAP-based per-prediction explainability instead of rule-based reasons
- Email delivery of PDF reports
- Dockerized deployment with Postgres for production scale
