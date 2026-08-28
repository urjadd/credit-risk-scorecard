import streamlit as st
import requests
import time

st.set_page_config(
    page_title="Credit Risk Scorecard",
    page_icon="🏦",
    layout="wide"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    .stApp {
        background-color: #0a0e17;
        color: #e2e8f0;
        font-family: 'Inter', sans-serif;
    }

    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        animation: fadeInDown 0.6s ease-out;
    }

    @keyframes fadeInDown {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }

    @keyframes scaleIn {
        from { opacity: 0; transform: scale(0.8); }
        to { opacity: 1; transform: scale(1); }
    }

    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    @keyframes countUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes pulse {
        0%, 100% { box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.4); }
        50% { box-shadow: 0 0 0 10px rgba(37, 99, 235, 0); }
    }

    @keyframes glowPulse {
        0%, 100% { opacity: 0.4; }
        50% { opacity: 1; }
    }

    @keyframes barFill {
        from { width: 0%; }
        to { width: var(--fill-width); }
    }

    .main-header h1 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        font-size: 2.2rem;
        color: #f8fafc;
        letter-spacing: -0.03em;
        margin: 0;
    }

    .main-header p {
        color: #64748b;
        font-size: 1rem;
        margin-top: 0.5rem;
        font-weight: 300;
    }

    .tag-line {
        display: inline-block;
        background: linear-gradient(135deg, #1e3a5f, #0f2940);
        color: #38bdf8;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 500;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-bottom: 1rem;
        border: 1px solid #1e4976;
    }

    .section-box {
        background: #0f1420;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        color: #38bdf8;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 600;
        margin-bottom: 0.25rem;
    }

    .section-desc {
        color: #475569;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }

    .field-help {
        color: #475569;
        font-size: 0.72rem;
        margin-top: -0.5rem;
        margin-bottom: 0.75rem;
    }

    .score-container {
        background: linear-gradient(145deg, #0f1a2e, #0a1220);
        border: 1px solid #1e293b;
        border-radius: 16px;
        padding: 2.5rem;
        text-align: center;
        margin: 1rem 0;
        animation: scaleIn 0.5s ease-out;
    }

    .score-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 5rem;
        font-weight: 700;
        line-height: 1;
        margin: 0.5rem 0;
        animation: countUp 0.8s ease-out;
    }

    .score-label {
        color: #64748b;
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.1em;
        font-weight: 500;
    }

    .score-low { color: #4ade80; text-shadow: 0 0 30px rgba(74, 222, 128, 0.3); }
    .score-medium { color: #fbbf24; text-shadow: 0 0 30px rgba(251, 191, 36, 0.3); }
    .score-high { color: #f87171; text-shadow: 0 0 30px rgba(248, 113, 113, 0.3); }

    .band-badge {
        display: inline-block;
        padding: 0.4rem 1.2rem;
        border-radius: 999px;
        font-size: 0.85rem;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 0.5rem;
        animation: fadeIn 1s ease-out;
    }

    .band-LOW { background: rgba(74, 222, 128, 0.1); color: #4ade80; border: 1px solid rgba(74, 222, 128, 0.3); }
    .band-MEDIUM { background: rgba(251, 191, 36, 0.1); color: #fbbf24; border: 1px solid rgba(251, 191, 36, 0.3); }
    .band-HIGH { background: rgba(248, 113, 113, 0.1); color: #f87171; border: 1px solid rgba(248, 113, 113, 0.3); }

    .metric-card {
        background: #0f1420;
        border: 1px solid #1e293b;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        transition: border-color 0.3s, transform 0.2s;
    }

    .metric-card:hover { border-color: #38bdf8; transform: translateY(-2px); }

    .metric-card .metric-value {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.8rem;
        font-weight: 600;
        color: #f8fafc;
    }

    .metric-card .metric-label {
        color: #64748b;
        font-size: 0.75rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }

    .metric-left { animation: slideInLeft 0.6s ease-out 0.3s both; }
    .metric-right { animation: slideInRight 0.6s ease-out 0.3s both; }

    .factor-card {
        background: #0f1420;
        border: 1px solid #1e293b;
        border-radius: 10px;
        padding: 1rem 1.25rem;
        margin: 0.5rem 0;
        display: flex;
        align-items: center;
        gap: 1rem;
        transition: border-color 0.3s, transform 0.2s;
    }

    .factor-card:hover { border-color: #334155; transform: translateX(4px); }

    .factor-anim-1 { animation: slideInLeft 0.4s ease-out 0.5s both; }
    .factor-anim-2 { animation: slideInLeft 0.4s ease-out 0.65s both; }
    .factor-anim-3 { animation: slideInLeft 0.4s ease-out 0.8s both; }

    .factor-icon-risk {
        width: 10px; height: 10px; border-radius: 50%;
        background: #f87171; flex-shrink: 0;
        box-shadow: 0 0 8px rgba(248, 113, 113, 0.4);
        animation: glowPulse 2s ease-in-out infinite;
    }

    .factor-icon-safe {
        width: 10px; height: 10px; border-radius: 50%;
        background: #4ade80; flex-shrink: 0;
        box-shadow: 0 0 8px rgba(74, 222, 128, 0.4);
        animation: glowPulse 2s ease-in-out infinite;
    }

    .factor-name { color: #e2e8f0; font-weight: 500; font-size: 0.95rem; }
    .factor-direction { color: #64748b; font-size: 0.8rem; margin-left: auto; }

    .factor-bar {
        height: 4px; border-radius: 2px; margin-top: 0.4rem;
        animation: barFill 0.8s ease-out forwards;
    }

    .factor-bar-risk { background: linear-gradient(to right, rgba(248, 113, 113, 0.2), #f87171); }
    .factor-bar-safe { background: linear-gradient(to right, rgba(74, 222, 128, 0.2), #4ade80); }

    .explanation-box {
        background: linear-gradient(145deg, #0f1a2e, #0a1220);
        border: 1px solid #1e3a5f;
        border-left: 3px solid #38bdf8;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        color: #cbd5e1;
        font-size: 0.95rem;
        line-height: 1.7;
        animation: fadeInUp 0.5s ease-out 1s both;
    }

    .reason-item {
        background: #0f1420;
        border: 1px solid #1e293b;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        margin: 0.4rem 0;
        color: #cbd5e1;
        font-size: 0.9rem;
        transition: border-color 0.3s, transform 0.2s;
    }

    .reason-item:hover { border-color: #38bdf8; transform: translateX(4px); }

    .reason-anim-1 { animation: slideInLeft 0.4s ease-out 0.9s both; }
    .reason-anim-2 { animation: slideInLeft 0.4s ease-out 1.0s both; }
    .reason-anim-3 { animation: slideInLeft 0.4s ease-out 1.1s both; }

    .reason-number {
        color: #38bdf8;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 600;
        margin-right: 0.5rem;
    }

    .result-header {
        color: #f8fafc;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #1e293b;
    }

    .stButton > button {
        width: 100%;
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        color: white;
        border: none;
        padding: 0.85rem 2rem;
        border-radius: 10px;
        font-weight: 600;
        font-size: 1.05rem;
        letter-spacing: 0.02em;
        transition: all 0.3s;
        animation: pulse 2s infinite;
        margin-top: 1rem;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #2563eb, #3b82f6);
        box-shadow: 0 4px 25px rgba(37, 99, 235, 0.4);
        transform: translateY(-1px);
    }

    div[data-testid="stNumberInput"] input,
    div[data-testid="stSelectbox"] > div > div {
        background: #0a0e17 !important;
        border-color: #1e293b !important;
        color: #e2e8f0 !important;
    }

    .scale-bar-bg {
        width: 100%; height: 6px; border-radius: 3px;
        background: #1e293b;
        margin: 1rem 0 0.5rem 0;
        position: relative; overflow: visible;
    }

    .scale-bar-fill {
        height: 100%; border-radius: 3px;
        background: linear-gradient(to right, #f87171, #fbbf24, #4ade80);
        animation: barFill 1.2s ease-out forwards;
    }

    .scale-labels {
        display: flex; justify-content: space-between;
        color: #475569; font-size: 0.7rem;
        font-family: 'JetBrains Mono', monospace;
    }

    .score-needle {
        position: absolute; top: -4px;
        width: 14px; height: 14px; border-radius: 50%;
        background: #f8fafc; border: 2px solid #0a0e17;
        box-shadow: 0 0 10px rgba(248, 250, 252, 0.5);
        transform: translateX(-50%);
        animation: fadeIn 1s ease-out 0.8s both;
    }

    .divider {
        border: none;
        border-top: 1px solid #1e293b;
        margin: 2rem 0;
    }

    .footer-note {
        text-align: center; color: #334155; font-size: 0.75rem;
        margin-top: 3rem; padding: 1rem; border-top: 1px solid #1e293b;
    }
</style>
""", unsafe_allow_html=True)

API_URL = "http://127.0.0.1:8000"

st.markdown("""
<div class="main-header">
    <span class="tag-line">AI-Powered Credit Decisioning</span>
    <h1>Credit Risk Scorecard</h1>
    <p>Enter applicant details below to generate a credit score, risk assessment, and plain English explanation.</p>
</div>
""", unsafe_allow_html=True)

# SECTION 1: CREDIT BUREAU SCORES
st.markdown("""
<div class="section-title">Section 1 of 4: Credit Bureau Scores</div>
<div class="section-desc">External credit scores from bureaus like CIBIL or Experian. Values range from 0 to 1, where higher means better credit history. Leave empty if bureau data is unavailable.</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    EXT_SOURCE_1 = st.number_input("Bureau Score 1", value=0.5, min_value=0.0, max_value=1.0, step=0.01)
    st.markdown('<p class="field-help">Primary bureau score (0 = worst, 1 = best)</p>', unsafe_allow_html=True)
with col2:
    EXT_SOURCE_2 = st.number_input("Bureau Score 2", value=0.5, min_value=0.0, max_value=1.0, step=0.01)
    st.markdown('<p class="field-help">Secondary bureau score (0 = worst, 1 = best)</p>', unsafe_allow_html=True)
with col3:
    EXT_SOURCE_3 = st.number_input("Bureau Score 3", value=0.5, min_value=0.0, max_value=1.0, step=0.01)
    st.markdown('<p class="field-help">Tertiary bureau score (0 = worst, 1 = best)</p>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# SECTION 2: APPLICANT PROFILE
st.markdown("""
<div class="section-title">Section 2 of 4: Applicant Profile</div>
<div class="section-desc">Personal and employment details of the loan applicant.</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    AGE_YEARS = st.number_input("Age (years)", value=35, min_value=18, max_value=80)
    st.markdown('<p class="field-help">Applicant must be 18 or older</p>', unsafe_allow_html=True)

    YEARS_EMPLOYED = st.number_input("Years at Current Job", value=5, min_value=0, max_value=50)
    st.markdown('<p class="field-help">Total years in current employment. 0 if unemployed.</p>', unsafe_allow_html=True)

with col2:
    OCCUPATION_TYPE = st.selectbox("Occupation", [
        "Laborers", "Sales staff", "Core staff", "Managers", "Drivers",
        "High skill tech staff", "Accountants", "Medicine staff", "Cooking staff",
        "Security staff", "Cleaning staff", "Private service staff",
        "Low-skill Laborers", "Secretaries", "Waiters/barmen staff",
        "Realty agents", "HR staff", "IT staff"
    ])
    st.markdown('<p class="field-help">Current job role of the applicant</p>', unsafe_allow_html=True)

    ORGANIZATION_TYPE = st.selectbox("Employer Type", [
        "Business Entity Type 3", "Business Entity Type 2", "Business Entity Type 1",
        "Self-employed", "Government", "Medicine", "School", "Trade: type 7",
        "Construction", "Transport: type 4", "Industry: type 9", "Military", "Other"
    ])
    st.markdown('<p class="field-help">Type of organization the applicant works for</p>', unsafe_allow_html=True)

with col3:
    NAME_INCOME_TYPE = st.selectbox("Income Source", ["Working", "Commercial associate", "Pensioner", "State servant", "Student"])
    st.markdown('<p class="field-help">How the applicant earns their income</p>', unsafe_allow_html=True)

    NAME_EDUCATION_TYPE = st.selectbox("Education Level", ["Higher education", "Secondary / secondary special", "Incomplete higher", "Lower secondary", "Academic degree"])
    st.markdown('<p class="field-help">Highest education completed</p>', unsafe_allow_html=True)

    NAME_FAMILY_STATUS = st.selectbox("Marital Status", ["Married", "Single / not married", "Civil marriage", "Separated", "Widow"])
    st.markdown('<p class="field-help">Current family status</p>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# SECTION 3: LOAN DETAILS
st.markdown("""
<div class="section-title">Section 3 of 4: Loan Details</div>
<div class="section-desc">The loan amount being requested and the proposed monthly repayment.</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    AMT_CREDIT = st.number_input("Loan Amount Requested", value=500000.0, min_value=0.0, step=10000.0, format="%.0f")
    st.markdown('<p class="field-help">Total loan amount in local currency (e.g. 500000)</p>', unsafe_allow_html=True)
with col2:
    AMT_ANNUITY = st.number_input("Monthly Payment (EMI)", value=25000.0, min_value=0.0, step=1000.0, format="%.0f")
    st.markdown('<p class="field-help">Proposed monthly repayment amount</p>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# SECTION 4: STABILITY INDICATORS
st.markdown("""
<div class="section-title">Section 4 of 4: Stability Indicators</div>
<div class="section-desc">How long the applicant has maintained their phone number, ID document, and registration. Enter as negative days from today (e.g. -500 means 500 days ago). Longer history means more stability.</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    DAYS_LAST_PHONE_CHANGE = st.number_input("Days Since Phone Change", value=-500, max_value=0)
    st.markdown('<p class="field-help">Negative number. -500 means phone was changed 500 days ago.</p>', unsafe_allow_html=True)

    REGION_POPULATION_RELATIVE = st.number_input("Region Population (relative)", value=0.03, min_value=0.0, max_value=0.1, step=0.005, format="%.3f")
    st.markdown('<p class="field-help">How populated is the applicant region (0.0 to 0.1)</p>', unsafe_allow_html=True)

with col2:
    DAYS_ID_PUBLISH = st.number_input("Days Since ID Issued", value=-3000, max_value=0)
    st.markdown('<p class="field-help">Negative number. -3000 means ID was issued 3000 days ago.</p>', unsafe_allow_html=True)

    REGION_RATING_CLIENT_W_CITY = st.selectbox("Region Credit Rating", [1, 2, 3])
    st.markdown('<p class="field-help">1 = best rated region, 3 = worst rated region</p>', unsafe_allow_html=True)

with col3:
    DAYS_REGISTRATION = st.number_input("Days Since Registration", value=-4000, max_value=0)
    st.markdown('<p class="field-help">Negative number. -4000 means registered 4000 days ago.</p>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# SCORE BUTTON
use_llm = st.checkbox("Include AI-generated plain English explanation", value=True)
run_prediction = st.button("Score This Applicant", type="primary")

if "result" not in st.session_state:
    st.session_state.result = None

if run_prediction:
    payload = {
        "EXT_SOURCE_1": EXT_SOURCE_1,
        "EXT_SOURCE_2": EXT_SOURCE_2,
        "EXT_SOURCE_3": EXT_SOURCE_3,
        "YEARS_EMPLOYED": YEARS_EMPLOYED,
        "AGE_YEARS": AGE_YEARS,
        "OCCUPATION_TYPE": OCCUPATION_TYPE,
        "ORGANIZATION_TYPE": ORGANIZATION_TYPE,
        "NAME_INCOME_TYPE": NAME_INCOME_TYPE,
        "NAME_EDUCATION_TYPE": NAME_EDUCATION_TYPE,
        "DAYS_LAST_PHONE_CHANGE": DAYS_LAST_PHONE_CHANGE,
        "AMT_CREDIT": AMT_CREDIT,
        "DAYS_ID_PUBLISH": DAYS_ID_PUBLISH,
        "REGION_POPULATION_RELATIVE": REGION_POPULATION_RELATIVE,
        "REGION_RATING_CLIENT_W_CITY": REGION_RATING_CLIENT_W_CITY,
        "DAYS_REGISTRATION": DAYS_REGISTRATION,
        "AMT_ANNUITY": AMT_ANNUITY,
        "NAME_FAMILY_STATUS": NAME_FAMILY_STATUS
    }

    endpoint = "/explain" if use_llm else "/predict"

    try:
        progress = st.empty()
        progress_bar = st.progress(0)

        steps = [
            "Validating applicant data...",
            "Running WOE transformation...",
            "Computing credit score...",
            "Calculating SHAP values...",
        ]
        if use_llm:
            steps.append("Generating AI explanation...")

        for i, step in enumerate(steps):
            progress.markdown(f"<p style='color: #38bdf8; font-size: 0.85rem; text-align: center;'>{step}</p>", unsafe_allow_html=True)
            if i == len(steps) - 1:
                response = requests.post(f"{API_URL}{endpoint}", json=payload)
                result = response.json()
                st.session_state.result = result
            else:
                time.sleep(0.3)
            progress_bar.progress((i + 1) / len(steps))

        progress.empty()
        progress_bar.empty()

    except requests.exceptions.ConnectionError:
        st.error("Cannot connect to the scoring API. Make sure the FastAPI server is running on port 8000.")
        st.session_state.result = None
    except Exception as e:
        st.error(f"Error: {str(e)}")
        st.session_state.result = None

if st.session_state.result:
    result = st.session_state.result
    score = result["credit_score"]
    band = result["risk_band"]
    proba = result["probability_of_default"]

    score_class = "score-low" if band == "LOW" else "score-medium" if band == "MEDIUM" else "score-high"
    needle_pos = ((score - 300) / 600) * 100

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    st.markdown(f"""
    <div class="score-container">
        <div class="score-label">Credit Score</div>
        <div class="score-value {score_class}">{score}</div>
        <div class="scale-bar-bg" style="position: relative;">
            <div class="scale-bar-fill" style="--fill-width: 100%;"></div>
            <div class="score-needle" style="left: {needle_pos}%;"></div>
        </div>
        <div class="scale-labels">
            <span>300 HIGH RISK</span>
            <span>600</span>
            <span>900 LOW RISK</span>
        </div>
        <div style="margin-top: 1rem;">
            <span class="band-badge band-{band}">{band} RISK</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_m1, col_m2, col_m3 = st.columns(3)

    with col_m1:
        st.markdown(f"""
        <div class="metric-card metric-left">
            <div class="metric-label">Default Probability</div>
            <div class="metric-value">{proba:.1%}</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m2:
        dti = (AMT_ANNUITY * 12) / AMT_CREDIT * 100 if AMT_CREDIT > 0 else 0
        st.markdown(f"""
        <div class="metric-card" style="animation: fadeInUp 0.6s ease-out 0.4s both;">
            <div class="metric-label">Annual Payment Ratio</div>
            <div class="metric-value">{dti:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

    with col_m3:
        verdict = "APPROVE" if band == "LOW" else "REVIEW" if band == "MEDIUM" else "DECLINE"
        verdict_color = "#4ade80" if band == "LOW" else "#fbbf24" if band == "MEDIUM" else "#f87171"
        st.markdown(f"""
        <div class="metric-card metric-right">
            <div class="metric-label">Recommended Action</div>
            <div class="metric-value" style="color: {verdict_color};">{verdict}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="result-header" style="animation: fadeIn 0.5s ease-out 0.5s both;">Decision Factors (SHAP)</div>', unsafe_allow_html=True)

    for i, factor in enumerate(result["top_shap_factors"]):
        direction = factor["direction"]
        icon_class = "factor-icon-risk" if direction == "increases_risk" else "factor-icon-safe"
        bar_class = "factor-bar-risk" if direction == "increases_risk" else "factor-bar-safe"
        feature = factor["feature"].replace("_", " ").title()
        direction_label = "Increases Risk" if direction == "increases_risk" else "Decreases Risk"
        bar_width = min(abs(factor["shap_value"]) * 200, 100)

        st.markdown(f"""
        <div class="factor-card factor-anim-{i+1}">
            <div class="{icon_class}"></div>
            <div style="flex: 1;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div class="factor-name">{feature}</div>
                    <div class="factor-direction">{direction_label}</div>
                </div>
                <div class="factor-bar {bar_class}" style="--fill-width: {bar_width}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if "reason_codes" in result:
        st.markdown('<div class="result-header" style="animation: fadeIn 0.5s ease-out 0.8s both;">Adverse Action Reasons (ECOA)</div>', unsafe_allow_html=True)

        for i, reason in enumerate(result["reason_codes"], 1):
            st.markdown(f"""
            <div class="reason-item reason-anim-{i}">
                <span class="reason-number">{i:02d}</span>{reason}
            </div>
            """, unsafe_allow_html=True)

    if "llm_explanation" in result and result["llm_explanation"]:
        st.markdown('<div class="result-header" style="animation: fadeIn 0.5s ease-out 1s both;">Plain English Explanation</div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="explanation-box">
            {result["llm_explanation"]}
        </div>
        """, unsafe_allow_html=True)

st.markdown("""
<div class="footer-note">
    Built on Home Credit Default Risk dataset (307K applications) · Logistic Regression + WOE + SHAP · FastAPI + Groq LLM
</div>
""", unsafe_allow_html=True)