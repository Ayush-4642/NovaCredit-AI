<div align="center">

# 💠 NovaCredit AI

### 🏦 AI-Powered Banking Risk Intelligence


⭐ **If you like this project, give it a star — it means a lot!** ⭐

[🚀 Live Demo - https://novacredit-ai-1.onrender.com](#) · [🐞 Report Bug](#) · [💡 Request Feature](#)

</div>


---

## 📚 Table of Contents

- [✨ Why NovaCredit AI?](#-why-novacredit-ai)
- [🚀 Features](#-features)
- [🧠 How the ML Pipeline Works](#-how-the-ml-pipeline-works)
- [🛠️ Tech Stack](#️-tech-stack)
- [🗺️ Architecture](#️-architecture)
- [📁 Project Structure](#-project-structure)
- [⚙️ Installation](#️-installation)
- [▶️ Usage](#️-usage)
- [🖼️ Screenshots](#️-screenshots)
- [🗺️ Routes Overview](#️-routes-overview)
- [📊 Model Performance](#-model-performance)
- [🔮 Roadmap](#-roadmap)
- [🤝 Contributing](#-contributing)
- [❓ FAQ](#-faq)
- [📄 License](#-license)

---

## ✨ Why NovaCredit AI?

Banks lose millions to bad loans that could've been flagged early. **NovaCredit AI** turns a trained Random Forest model into a real, usable product — not just a Jupyter notebook. Enter applicant details, get an instant, explainable risk verdict, and track your entire portfolio's health from one beautiful dashboard.

> 💡 Built to prove that a data science pipeline can become a genuinely production-feeling FinTech app — form → prediction → storage → analytics → reporting, all wired together.

---

## 🚀 Features

### 🎯 Prediction Engine
- Guided **3-step form** (Customer → Financial → Loan Info) with live validation
- Instant prediction via a pre-trained **Random Forest Classifier**
- Animated **risk gauge** + probability-of-default score
- 💡 Explainable, plain-language risk factors & recommendations

### 📊 Analytics & Insights
- 9+ **interactive Chart.js** visualizations: age, income, credit score, loan purpose, city-wise counts, monthly trend, feature importance, risk split
- 👥 Customer statistics dashboard with portfolio-wide aggregates
- 🛡️ Admin control center with live KPIs and recent activity feed

### 🗂️ Data & Reporting
- Full prediction **history** — search 🔍, sort ↕️, filter 🎚️, paginate, delete 🗑️
- 📄 Branded **PDF reports** per prediction (ReportLab) + printable browser view
- ⬇️ Export entire history to **CSV** or **PDF**

### 🎨 Design
- 💎 Glassmorphism FinTech UI — dark navy + purple, gradient accents
- 🌗 **Dark / Light mode** toggle, remembered via `localStorage`
- 📱 Fully responsive — desktop, tablet, mobile

---

## 🧠 How the ML Pipeline Works
📄 Applicant Form

↓

✅ Validate Input

↓

🌲 Random Forest Classifier (random_forest_model.pkl)

↓

📊 Prediction + Probability

↓

💡 Rule-Based Recommendation Engine

↓

💾 Auto-Saved to SQLite

↓

📈 Instantly Reflected in Analytics

## ⚠️ Important: How Predictions Actually Work

`Model_Training.ipynb` trains the **Random Forest** model directly on **raw, unscaled** feature values — `StandardScaler` in that notebook is only used for the KNN/MLP experiments, never for the Random Forest.

To stay faithful to how the model was actually trained, `models/predictor.py`:
- ✅ Feeds **raw** feature values into `random_forest_model.pkl`
- ❌ Does **not** apply `scaler.pkl` before that prediction

Applying the scaler here would put the model's inputs on a completely different scale than it saw during training and silently corrupt every prediction. `scaler.pkl` is still loaded and available in the codebase for transparency and any future model that needs it.

---

## 🛠️ Tech Stack

<div align="center">

| Layer | Technology |
|:---:|:---:|
| 🎨 Frontend | HTML5 · CSS3 · JavaScript · Chart.js |
| ⚙️ Backend | Python · Flask |
| 🗄️ Database | SQLite |
| 🤖 Machine Learning | scikit-learn (Random Forest) |
| 📄 PDF Engine | ReportLab |

---

## 📁 Project Structure

NovaCredit-AI/

├── app.py                     # Flask app factory & entry point

├── config.py                  # Paths, feature order, pagination config

├── requirements.txt

├── random_forest_model.pkl    # Pre-trained model

├── scaler.pkl                 # Pre-trained scaler

├── banking_risk_analytics_dataset.csv

├── EDA.ipynb

├── Model_Training.ipynb

│
├── database/

│   ├── database.py            # Schema, CRUD, aggregate queries

│   └── banking.db             # Auto-created on first run

│

├── models/

│   └── predictor.py           # Loads artifacts, runs inference, recommendations

│

├── utils/

│   └── pdf_report.py          # ReportLab PDF generation

│

├── routes/

│   ├── home.py

│   ├── predict.py

│   ├── analytics.py

│   ├── dashboard.py

│   ├── history.py

│   └── admin.py

│

├── templates/                 # Jinja2 templates

├── static/

│   ├── css/style.css          # Design system, dark/light theme

│   └── js/script.js, charts.js

│

├── reports/                   # Generated PDF reports

├── exports/                   # Generated CSV/PDF exports

---

## 🗺️ Routes Overview

| Route | Description |
|---|---|
| `/` | 🏠 Home — hero, animated stats, features |
| `/predict` | 🎯 Multi-step loan risk prediction form |
| `/predict/result/<id>` | 📊 Prediction result with gauge & recommendations |
| `/predict/report/<id>` | 📄 Download branded PDF report |
| `/history` | 📜 Full prediction history |
| `/analytics` | 📈 Interactive analytics dashboard |
| `/dashboard` | 👥 Customer statistics |
| `/admin` | 🛡️ Admin control center |
| `/about` | ℹ️ Project & model information |

## 📊 Model Performance

| Metric | Score |
|---|---|
| Accuracy | ~64.5% |
| Algorithm | Random Forest Classifier |
| Top Feature | Credit Score |

---

## 🔮 Roadmap

- [ ] 🔐 User authentication & role-based access
- [ ] 🧪 Model versioning + A/B testing (RF vs KNN vs MLP)
- [ ] 🧠 SHAP-based per-prediction explainability
- [ ] 📧 Email delivery of PDF reports
- [ ] 🐳 Docker + PostgreSQL for production deployment

---

## ❓ FAQ

**Q: Does this retrain the model every time?**
No — it loads the existing `random_forest_model.pkl` and runs inference only.

**Q: Why isn't the scaler applied before prediction?**
Because the Random Forest was trained on raw, unscaled data — see [How the ML Pipeline Works](#-how-the-ml-pipeline-works).

**Q: Can I use my own dataset?**
Yes — retrain using `Model_Training.ipynb` and drop the new `.pkl` files into the project root.

---


### 💜 Made with passion, Python, and a lot of ☕

**If this project helped you, consider giving it a ⭐!**

