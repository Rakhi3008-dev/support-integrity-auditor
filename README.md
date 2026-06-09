# 🛡️ Support Integrity Auditor

An AI-powered system for detecting inconsistencies between human-assigned support ticket priorities and inferred ticket severity.

## 🚀 Problem Statement

Customer support teams manually assign priorities to incoming tickets. However, human-assigned priorities may not always reflect the true severity of an issue.

This project identifies:

* 🔴 **Hidden Crises** — Tickets that appear more severe than their assigned priority.
* 🟡 **False Alarms** — Tickets that appear less severe than their assigned priority.
* 🟢 **Consistent Tickets** — Tickets where assigned priority aligns with inferred severity.

The system combines NLP, self-supervised learning, feature engineering, explainable AI, and machine learning to perform automated ticket audits.

---

## ✨ Features

### 📊 Exploratory Data Analysis (EDA)

* Priority distribution analysis
* Issue category analysis
* Resolution time analysis
* Text length analysis
* Dataset quality assessment

### 🧠 Severity Inference Engine

Severity is inferred using multiple signals:

* Semantic urgency score
* Keyword severity score
* Resolution-time severity score

These signals are combined into a unified severity score.

### 🏷️ Self-Supervised Pseudo Labeling

The system generates labels without manual annotation by comparing:

Assigned Priority ↔ Inferred Severity

Generated classes:

* Hidden Crisis
* False Alarm
* Consistent

### 🤖 Machine Learning Classifier

Model:

* XGBoost Classifier

Features:

* Ticket text (TF-IDF)
* Issue category
* Ticket channel
* Resolution time
* Engineered severity features

### 📋 Explainable Evidence Dossier

For every flagged ticket, the system generates:

* Assigned Priority
* Inferred Severity
* Mismatch Type
* Severity Delta
* Detected Keywords
* Semantic Score
* Resolution Analysis
* AI Explanation
* Confidence Score

### 🌐 Streamlit Web Application

Interactive dashboard for:

* Single-ticket auditing
* Priority mismatch detection
* Evidence generation
* AI explanations

---

## 🏗️ Project Architecture

```text
Customer Support Ticket
            │
            ▼
     Feature Engineering
            │
            ├── Keyword Score
            ├── Semantic Score
            └── Resolution Score
            │
            ▼
    Severity Calibration
            │
            ▼
     Inferred Severity
            │
            ▼
    Pseudo Label Generation
            │
            ▼
      XGBoost Classifier
            │
            ▼
    Evidence Dossier Engine
            │
            ▼
      Streamlit Dashboard
```

---

## 📂 Project Structure

```text
Support-Integrity-Auditor/

├── data/
│   ├── customer_support_tickets.csv
│   ├── pseudo_labeled_tickets.csv
│   └── evidence_dossiers.json
│
├── models/
│   └── xgb_pipeline.pkl
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_Pseudo_Label_Generation.ipynb
│   ├── 03_Classifier_Training.ipynb
│   └── 04_Evidence_Dossier_Generation.ipynb
│
├── src/
│   ├── preprocess.py
│   ├── feature_engineering.py
│   ├── pseudo_label.py
│   ├── train.py
│   ├── inference.py
│   └── evidence_generator.py
│
├── app.py
├── predict.py
├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

* Python
* Pandas
* NumPy
* Scikit-Learn
* XGBoost
* Sentence Transformers
* Streamlit
* Joblib

---

## 📈 Model Performance

| Metric                     | Score |
| -------------------------- | ----- |
| Accuracy                   | 76.1% |
| Recall (Mismatch Class)    | 81.0% |
| Precision (Mismatch Class) | 54.0% |
| Macro F1 Score             | 0.73  |

The model is intentionally optimized for high recall to reduce the likelihood of missing genuine Hidden Crisis tickets.

---
## Ablation Study

To evaluate the contribution of each severity signal, we trained a Logistic Regression classifier using different combinations of engineered features.

| Configuration         | Accuracy   |
| --------------------- | ---------- |
| Semantic Only         | 72.80%     |
| Keyword Only          | 72.80%     |
| Resolution Only       | 72.80%     |
| Semantic + Keyword    | **75.95%** |
| Semantic + Resolution | 72.90%     |
| Keyword + Resolution  | 73.08%     |
| Full Fusion           | 73.33%     |

### Observations

* Semantic and keyword-based signals provide the strongest predictive information.
* Combining semantic and keyword features improves performance by more than 3 percentage points over any individual signal.
* Resolution time contributes only marginally to predictive performance in this dataset.
* Although the full fusion configuration did not outperform the Semantic + Keyword combination, operational signals such as resolution time were retained to preserve interpretability and align with real-world support workflows.

These findings indicate that textual indicators are the primary drivers of priority mismatch detection, while operational metadata serves as a supplementary signal.


## ▶️ Run Locally

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Launch Application

```bash
streamlit run app.py
```

---

## 📋 Example Output

**Assigned Priority:** Medium

**Inferred Severity:** Critical

**Audit Result:** Hidden Crisis

**Confidence:** 95%

**Detected Keywords:**

* payment failed
* failed

**AI Explanation:**

The presence of payment-related failure indicators and a high semantic urgency score suggests that the ticket deserves a higher priority than the assigned Medium level.

---

## 🎯 Future Improvements

* Transformer-based classification (DeBERTa/BERT)
* Real-time ticket ingestion
* Batch auditing dashboard
* Advanced explainability using SHAP
* Cloud deployment and monitoring

---

## 👩‍💻 Author

Rakhi Jha

AI / ML | NLP | Explainable AI | Support Operations Analytics
