# Credit Risk Scorecard

An end-to-end credit risk scoring system built on the Home Credit Default Risk dataset (300k+ real loan applications).

## What This Does

Takes applicant financial data as input and returns a credit score, risk band, and plain English explanation of the decision. Built for loan officers, not data scientists.

## Project Structure
├── notebooks/          # EDA, modelling, and analysis
├── src/                # Reusable Python modules
├── models/             # Saved model artifacts
├── math-intuition/     # Plain English notes on model mathematics
├── docs/               # API docs, model card, runbook

## Tech Stack

- Data and EDA: pandas, matplotlib, seaborn, WOE encoding
- Model: scikit-learn Logistic Regression, SHAP
- Evaluation: Gini coefficient, KS statistic, AUC-ROC
- API: FastAPI, Pydantic, Uvicorn
- CI/CD: Docker, GitHub Actions, Render
- LLM Layer: Groq + SHAP explainability pipeline
- Frontend: Streamlit

## Status

| Stage | Status |
|---|---|
| Stage 1: Data and EDA | In Progress |
| Stage 2: Scorecard Model | Upcoming |
| Stage 3: FastAPI Endpoint | Upcoming |
| Stage 4: Cloud and CI/CD | Upcoming |
| Stage 5: LLM Explainability | Upcoming |
| Stage 6: Streamlit Dashboard | Upcoming |

## Dataset

Home Credit Default Risk, Kaggle. 307k rows, real lending data.
