import joblib
import numpy as np
import pandas as pd
import shap
import os
from fastapi import FastAPI
from schemas import ApplicantInput, CreditScoreResponse, SHAPFactor
from explainer import get_llm_explanation

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

model = joblib.load(os.path.join(BASE_DIR, "models", "logistic_model.pkl"))
binning_process = joblib.load(os.path.join(BASE_DIR, "models", "binning_process.pkl"))
scorecard_params = joblib.load(os.path.join(BASE_DIR, "models", "scorecard_params.pkl"))

explainer = shap.LinearExplainer(model, shap.maskers.Independent(np.zeros((1, len(binning_process.variable_names)))))

app = FastAPI(title="Credit Risk Scorecard API")


def calculate_credit_score(probability):
    factor = scorecard_params["factor"]
    offset = scorecard_params["offset"]

    odds = (1 - probability) / probability
    score = offset + factor * np.log(odds)
    return int(np.clip(score, 300, 900))


def get_risk_band(score):
    if score >= 700:
        return "LOW"
    elif score >= 500:
        return "MEDIUM"
    else:
        return "HIGH"


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/predict", response_model=CreditScoreResponse)
def predict(applicant: ApplicantInput):
    input_dict = applicant.model_dump()
    input_df = pd.DataFrame([input_dict])

    woe_df = binning_process.transform(input_df[binning_process.variable_names])

    proba = model.predict_proba(woe_df)[0][1]

    score = calculate_credit_score(proba)
    risk_band = get_risk_band(score)

    shap_values = explainer.shap_values(woe_df)
    feature_names = binning_process.variable_names

    shap_pairs = list(zip(feature_names, shap_values[0]))
    shap_pairs.sort(key=lambda x: abs(x[1]), reverse=True)
    top_3 = shap_pairs[:3]

    top_shap_factors = [
        SHAPFactor(
            feature=name,
            shap_value=round(float(val), 4),
            direction="increases_risk" if val > 0 else "decreases_risk"
        )
        for name, val in top_3
    ]

    return CreditScoreResponse(
        credit_score=score,
        risk_band=risk_band,
        probability_of_default=round(float(proba), 4),
        top_shap_factors=top_shap_factors
    )


@app.post("/explain")
def explain(applicant: ApplicantInput):
    input_dict = applicant.model_dump()
    input_df = pd.DataFrame([input_dict])

    woe_df = binning_process.transform(input_df[binning_process.variable_names])

    proba = model.predict_proba(woe_df)[0][1]

    score = calculate_credit_score(proba)
    risk_band = get_risk_band(score)

    shap_values = explainer.shap_values(woe_df)
    feature_names = binning_process.variable_names

    shap_pairs = list(zip(feature_names, shap_values[0]))
    shap_pairs.sort(key=lambda x: abs(x[1]), reverse=True)
    top_3 = shap_pairs[:3]

    shap_factors = [
        {"feature": name, "shap_value": round(float(val), 4), "direction": "increases_risk" if val > 0 else "decreases_risk"}
        for name, val in top_3
    ]

    explanation = get_llm_explanation(shap_factors, score, risk_band, proba)

    return {
        "credit_score": score,
        "risk_band": risk_band,
        "probability_of_default": round(float(proba), 4),
        "top_shap_factors": shap_factors,
        "reason_codes": explanation["reason_codes"],
        "llm_explanation": explanation["llm_explanation"]
    }