# Statement of Work: Credit Risk Scorecard
**Project:** Credit Risk Scorecard
**Version:** 1.0
**Date:** May 2026
**Author:** Urja Damodhar

---

## 1. Objective
Home Credit serves customers who lack formal credit history and 
cannot access traditional banking. The goal of this project is 
to build a credit scorecard that predicts the probability of 
loan default for each applicant, enabling loan officers to make 
faster, fairer, and more explainable lending decisions.

## 2. Business Problem
Home Credit serves applicants who are invisible to traditional credit bureaus: migrant workers, first-time borrowers, and people in the informal economy. Without a credit history, loan officers have no objective basis for decisions, so they either reject good applicants out of caution or rely on gut feel, which introduces bias. This scorecard solves that by using behavioural and financial signals to estimate default probability. If the model is too strict, creditworthy people are denied loans they need. If it is too lenient, the bank absorbs losses that threaten the viability of the lending programme itself.

## 3. Scope
**In scope:**
- EDA and feature selection using WOE and IV
- Logistic regression scorecard model
- SHAP explainability
- FastAPI prediction endpoint
- GitHub Actions CI/CD
- LLM plain English explanations
- Streamlit dashboard for loan officers

**Out of scope:**
- Real time transaction data
- Bureau and supplementary data files
- Model retraining pipeline

## 4. Deliverables
| Deliverable | Stage | Format |
|---|---|---|
| EDA findings report | Stage 1 | Markdown |
| Trained scorecard model | Stage 2 | .pkl file |
| Model card | Stage 2 | Markdown |
| API documentation | Stage 3 | Markdown |
| Deployment runbook | Stage 4 | Markdown |
| Math intuition notes | All | Markdown |
| Streamlit dashboard | Stage 6 | Live URL |

## 5. Success Criteria
- The model must achieve a Gini coefficient of at least 45 on the held-out test set.
- All three pillars complete for every stage
- Live API endpoint running without errors
- Dashboard usable by a non-technical loan officer

## 6. Tech Stack
| Component | Tool | Reason |
|---|---|---|
| Data and EDA | pandas, matplotlib, seaborn | Industry standard for data manipulation and visual exploration in Python |
| Feature selection | WOE, IV | Designed specifically for binary classification in credit risk. Transforms categories into log-odds scale which logistic regression natively works in |
| Model | Logistic Regression | Interpretable, monotonic, and accepted by financial regulators. XGBoost is more accurate but cannot be used in regulated credit decisions without additional justification |
| Explainability | SHAP | Assigns each feature a contribution score for individual predictions. Required for adverse action notices under lending regulations |
| API | FastAPI | Fast, async, automatic Swagger documentation. Lets frontend teams consume the model without touching Python |
| CI/CD | GitHub Actions | Automates testing on every pull request and deployment on merge. Creates the audit trail that compliance teams require in regulated finance |
| Frontend | Streamlit | Rapid dashboard deployment without frontend engineering. Sufficient for internal loan officer tooling |

## 7. Constraints and Risks
- Dataset has ~8% default rate: class imbalance means a naive model 
  that predicts no default for everyone achieves 92% accuracy but is 
  completely useless. Evaluation must use Gini and KS, not accuracy.
- Regulatory constraint: under ECOA (Equal Credit Opportunity Act), 
  lenders must provide specific reasons when declining credit. The model 
  cannot be a black box. Every declined application must produce an 
  explainable adverse action notice, which is why SHAP is non-negotiable.
- Data quality risk: several features have over 40% missing values. 
  Imputation choices made during EDA will directly affect model fairness 
  and performance. Poor imputation could introduce bias against certain 
  applicant groups.

## 8. Timeline
| Stage | Description | Deadline |
|---|---|---|
| Stage 1 | Data and EDA | Day 1 |
| Stage 2 | Scorecard Model | Day 2 |
| Stage 3 | FastAPI Endpoint | Day 3 |
| Stage 4 | Cloud and CI/CD | Day 3 |
| Stage 5 | LLM Explainability | Day 4 |
| Stage 6 | Streamlit Dashboard | Day 4 |

**Project Complete: Day 4**