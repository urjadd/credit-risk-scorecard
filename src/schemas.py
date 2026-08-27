from pydantic import BaseModel
from typing import Optional, List

class ApplicantInput(BaseModel):
    EXT_SOURCE_1: Optional[float] = None
    EXT_SOURCE_2: Optional[float] = None
    EXT_SOURCE_3: Optional[float] = None
    YEARS_EMPLOYED: int
    AGE_YEARS: int
    OCCUPATION_TYPE: Optional[str] = None
    ORGANIZATION_TYPE: str
    NAME_INCOME_TYPE: str
    NAME_EDUCATION_TYPE: str
    DAYS_LAST_PHONE_CHANGE: float
    AMT_CREDIT: float
    DAYS_ID_PUBLISH: int
    REGION_POPULATION_RELATIVE: float
    REGION_RATING_CLIENT_W_CITY: int
    DAYS_REGISTRATION: float
    AMT_ANNUITY: float
    NAME_FAMILY_STATUS: str


class SHAPFactor(BaseModel):
    feature: str
    shap_value: float
    direction: str  # "increases_risk" or "decreases_risk"


class CreditScoreResponse(BaseModel):
    credit_score: int
    risk_band: str
    probability_of_default: float
    top_shap_factors: List[SHAPFactor]