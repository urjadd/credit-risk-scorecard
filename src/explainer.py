import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

REASON_CODES = {
    "EXT_SOURCE_1": {"increases_risk": "External credit score 1 is low or unavailable", "decreases_risk": "External credit score 1 is strong"},
    "EXT_SOURCE_2": {"increases_risk": "External credit score 2 is low or unavailable", "decreases_risk": "External credit score 2 is strong"},
    "EXT_SOURCE_3": {"increases_risk": "External credit score 3 is low or unavailable", "decreases_risk": "External credit score 3 is strong"},
    "YEARS_EMPLOYED": {"increases_risk": "Employment history is short or unstable", "decreases_risk": "Employment history is stable and long-term"},
    "AGE_YEARS": {"increases_risk": "Applicant age indicates limited credit history", "decreases_risk": "Applicant age indicates mature credit profile"},
    "OCCUPATION_TYPE": {"increases_risk": "Occupation type is associated with higher default rates", "decreases_risk": "Occupation type is associated with lower default rates"},
    "ORGANIZATION_TYPE": {"increases_risk": "Employer type is associated with higher risk", "decreases_risk": "Employer type is associated with lower risk"},
    "NAME_INCOME_TYPE": {"increases_risk": "Income type carries elevated risk", "decreases_risk": "Income type is stable and reliable"},
    "NAME_EDUCATION_TYPE": {"increases_risk": "Education level is associated with higher default rates", "decreases_risk": "Education level is associated with lower default rates"},
    "AMT_CREDIT": {"increases_risk": "Loan amount is high relative to profile", "decreases_risk": "Loan amount is conservative relative to profile"},
    "AMT_ANNUITY": {"increases_risk": "Monthly payment burden is high", "decreases_risk": "Monthly payment burden is manageable"},
    "DAYS_LAST_PHONE_CHANGE": {"increases_risk": "Recent phone number change may indicate instability", "decreases_risk": "Phone number has been stable"},
    "DAYS_ID_PUBLISH": {"increases_risk": "ID document was issued recently", "decreases_risk": "ID document has been held for a long time"},
    "REGION_POPULATION_RELATIVE": {"increases_risk": "Applicant is from a sparsely populated region", "decreases_risk": "Applicant is from a well-populated region"},
    "REGION_RATING_CLIENT_W_CITY": {"increases_risk": "Region has a lower credit rating", "decreases_risk": "Region has a higher credit rating"},
    "DAYS_REGISTRATION": {"increases_risk": "Registration history is short", "decreases_risk": "Registration history is long and stable"},
    "NAME_FAMILY_STATUS": {"increases_risk": "Family status is associated with higher risk", "decreases_risk": "Family status is associated with lower risk"},
}


def get_reason_codes(shap_factors):
    reasons = []
    for factor in shap_factors:
        feature = factor["feature"]
        direction = factor["direction"]
        if feature in REASON_CODES:
            reasons.append(REASON_CODES[feature][direction])
        else:
            reasons.append(f"{feature} {'increases' if direction == 'increases_risk' else 'decreases'} risk")
    return reasons


def get_llm_explanation(shap_factors, credit_score, risk_band, probability):
    reason_codes = get_reason_codes(shap_factors)

    prompt = f"""You are a credit risk analyst writing an explanation for a loan officer.

Credit Score: {credit_score}
Risk Band: {risk_band}
Probability of Default: {probability:.1%}

Top factors driving this decision:
1. {reason_codes[0]}
2. {reason_codes[1]}
3. {reason_codes[2]}

Write a 3-4 sentence plain English explanation of this credit decision. No jargon. No technical terms. Write as if explaining to someone who has never seen a credit model. End with one sentence on what the applicant could do to improve their score."""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1024
    )
    print("LLM RESPONSE:", response.choices[0].message.content)
    print("FULL RESPONSE:", response.choices[0])
    return {
        "reason_codes": reason_codes,
        "llm_explanation": response.choices[0].message.content
    }