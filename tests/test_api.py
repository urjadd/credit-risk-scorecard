from fastapi.testclient import TestClient
import sys
sys.path.insert(0, "src")
from main import app

client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_valid():
    payload = {
        "EXT_SOURCE_1": 0.5,
        "EXT_SOURCE_2": 0.6,
        "EXT_SOURCE_3": 0.4,
        "YEARS_EMPLOYED": 5,
        "AGE_YEARS": 35,
        "OCCUPATION_TYPE": "Laborers",
        "ORGANIZATION_TYPE": "Business Entity Type 3",
        "NAME_INCOME_TYPE": "Working",
        "NAME_EDUCATION_TYPE": "Higher education",
        "DAYS_LAST_PHONE_CHANGE": -500,
        "AMT_CREDIT": 500000,
        "DAYS_ID_PUBLISH": -3000,
        "REGION_POPULATION_RELATIVE": 0.03,
        "REGION_RATING_CLIENT_W_CITY": 2,
        "DAYS_REGISTRATION": -4000,
        "AMT_ANNUITY": 25000,
        "NAME_FAMILY_STATUS": "Married"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "credit_score" in data
    assert data["risk_band"] in ["LOW", "MEDIUM", "HIGH"]
    assert 300 <= data["credit_score"] <= 900
    assert len(data["top_shap_factors"]) == 3


def test_predict_missing_required():
    payload = {"EXT_SOURCE_1": 0.5}
    response = client.post("/predict", json=payload)
    assert response.status_code == 422


def test_predict_with_nulls():
    payload = {
        "EXT_SOURCE_1": None,
        "EXT_SOURCE_2": 0.15,
        "EXT_SOURCE_3": None,
        "YEARS_EMPLOYED": 0,
        "AGE_YEARS": 22,
        "OCCUPATION_TYPE": None,
        "ORGANIZATION_TYPE": "Self-employed",
        "NAME_INCOME_TYPE": "Working",
        "NAME_EDUCATION_TYPE": "Secondary / secondary special",
        "DAYS_LAST_PHONE_CHANGE": -50,
        "AMT_CREDIT": 900000,
        "DAYS_ID_PUBLISH": -500,
        "REGION_POPULATION_RELATIVE": 0.01,
        "REGION_RATING_CLIENT_W_CITY": 3,
        "DAYS_REGISTRATION": -500,
        "AMT_ANNUITY": 55000,
        "NAME_FAMILY_STATUS": "Single / not married"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    assert response.json()["credit_score"] < 900