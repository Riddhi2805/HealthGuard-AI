import streamlit as st
import pandas as pd
from datetime import date

st.title("🩺 Health Risk Assessment")

st.write(
    "Answer a few questions to receive health risk insights and recommended screenings."
)

use_profile = st.checkbox(
    "Use My Profile Information",
    value=True
)

# Basic Information

st.subheader("Basic Information")

PROFILE_FILE = "data/user_profile.csv"

try:
    profile_df = pd.read_csv(
        PROFILE_FILE
    )
except:
    profile_df = pd.DataFrame()

# Sidebar

st.sidebar.title(
    "🏥 HealthGuard AI"
)

if not profile_df.empty:

    profile = profile_df.iloc[0]

    st.sidebar.success(
        f"👋 Welcome, {str(profile['Name']).title()}!"
    )

else:

    st.sidebar.success(
        "👋 Welcome, User!"
    )

st.sidebar.markdown("---")

st.sidebar.caption(
    "Empowering Preventive Healthcare Through AI"
)

if use_profile and profile_df.empty:

    st.warning(
        "No profile found.Please Fill the following information to get personalized health risk assessment."
    )

    use_profile = False

if use_profile:

    profile = profile_df.iloc[0]

    default_gender = profile["Gender"]

    dob = pd.to_datetime(
        profile["DOB"]
    ).date()

    today = date.today()

    default_age = (
        today.year
        - dob.year
        - (
            (today.month, today.day)
            <
            (dob.month, dob.day)
        )
    )

    default_height = float(
        profile["Height"]
    )

    default_weight = float(
        profile["Weight"]
    )

else:

    default_gender = "Select"

    default_age = 25

    default_height = 170.0

    default_weight = 70.0

gender_options = [
    "Select",
    "Male",
    "Female",
    "Other"
]

gender = st.selectbox(
    "Select Gender",
    gender_options,
    index=gender_options.index(
        default_gender
    ),
    disabled=use_profile
)


age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=default_age,
    disabled=use_profile
)

height = st.number_input(
    "Height (cm)",
    min_value=50.0,
    max_value=250.0,
    value=default_height,
    disabled=use_profile
)

weight = st.number_input(
    "Weight (kg)",
    min_value=10.0,
    max_value=300.0,
    value=default_weight,
    disabled=use_profile
)
    
# Symptoms

st.subheader("Symptoms")

fatigue = st.checkbox("Fatigue")
headache = st.checkbox("Frequent Headache")
thirst = st.checkbox("Excessive Thirst")
urination = st.checkbox("Frequent Urination")
chest_pain = st.checkbox("Chest Pain")
breath = st.checkbox("Shortness of Breath")
weight_loss = st.checkbox("Unexplained Weight Loss")

# Lifestyle

st.subheader("Lifestyle")

smoking = st.radio(
    "Do you smoke?",
    ["No", "Yes"]
)

exercise = st.selectbox(
    "Exercise Frequency",
    [
        "Regular",
        "Occasionally",
        "Rarely"
    ]
)

if st.button("Assess Risk"):

    if gender == "Select":

        st.warning(
            "Please select a gender."
        )

        st.stop()

    concerns = []
    tests = []
    risk_score = 0

    # ----------------------------------------------
    # BMI CALCULATION
    # ----------------------------------------------

    height_m = height / 100

    bmi = weight / (height_m ** 2)

    # ----------------------------------------------
    # DIABETES RISK
    # ----------------------------------------------

    if thirst and urination:

        concerns.append(
            "Possible Diabetes Risk"
        )

        tests.extend([
            "Blood Sugar Test",
            "HbA1c Test"
        ])

        risk_score += 2

    # ----------------------------------------------
    # CARDIAC RISK
    # ----------------------------------------------

    if chest_pain or breath:

        concerns.append(
            "Potential Cardiac Risk"
        )

        tests.extend([
            "ECG",
            "Lipid Profile",
            "Blood Pressure Check"
        ])

        risk_score += 3

    #----------------------------------------------
    # Headache Risk
    #----------------------------------------------
    if headache:

        concerns.append(
            "Possible Stress, Migraine, or Blood Pressure Concern"
        )

        tests.append(
            "Blood Pressure Check"
        )

        risk_score += 1

    #----------------------------------------------
    # Weight Loss Risk
    #----------------------------------------------
    if weight_loss:

        concerns.append(
            "Unexplained Weight Loss Requires Medical Evaluation"
        )

        tests.extend([
            "CBC",
            "Blood Sugar Test"
        ])

        risk_score += 2

    # ----------------------------------------------
    # THYROID / NUTRITIONAL RISK
    # ----------------------------------------------

    if fatigue:

        concerns.append(
            "Possible Nutritional or Thyroid Concern"
        )

        tests.extend([
            "CBC",
            "Thyroid Profile",
            "Vitamin D Test"
        ])

        risk_score += 1

    # ----------------------------------------------
    # SMOKING RISK
    # ----------------------------------------------

    if smoking == "Yes":

        concerns.append(
            "Smoking-Related Health Risk"
        )

        tests.append(
            "Lung Health Screening"
        )

        risk_score += 2

    # ----------------------------------------------
    # BMI RISK
    # ----------------------------------------------

    if bmi >= 30:

        concerns.append(
            "Obesity-Related Health Risk"
        )

        tests.extend([
            "Blood Sugar Test",
            "Lipid Profile",
            "Blood Pressure Check"
        ])

        risk_score += 2

    # ----------------------------------------------
    # EXERCISE RISK
    # ----------------------------------------------

    if exercise == "Rarely":

        risk_score += 1

    # ----------------------------------------------
    # AGE RISK
    # ----------------------------------------------

    if age >= 50:

        risk_score += 1

    # ----------------------------------------------
    # RESULTS
    # ----------------------------------------------

    st.header(
        "📋 Assessment Results"
    )

    st.subheader(
        f"BMI: {bmi:.2f}"
    )

    if risk_score <= 2:

        st.success(
            "🟢 Low Health Risk"
        )

    elif risk_score <= 5:

        st.warning(
            "🟡 Moderate Health Risk"
        )

    else:

        st.error(
            "🔴 High Health Risk"
        )

    # ----------------------------------------------
    # HEALTH CONCERNS
    # ----------------------------------------------

    if concerns:

        st.subheader(
            "⚠️ Potential Health Concerns"
        )

        for item in sorted(
            set(concerns)
        ):

            st.write(
                f"• {item}"
            )

    else:

        st.success(
            "No major risk indicators detected based on the provided information."
        )

    # ----------------------------------------------
    # RECOMMENDED TESTS
    # ----------------------------------------------

    if tests:

        st.subheader(
            "🧪 Recommended Tests"
        )

        for test in sorted(
            set(tests)
        ):

            st.write(
                f"✅ {test}"
            )

    # ----------------------------------------------
    # PREVENTIVE SCREENINGS
    # ----------------------------------------------

    st.subheader(
        "🩺 Recommended Preventive Screenings"
    )

    if age >= 40:

        st.write(
            "✅ Annual Blood Pressure Check"
        )

        st.write(
            "✅ Diabetes Screening"
        )

    if gender == "Female" and age >= 40:

        st.write(
            "✅ Mammography"
        )

    if gender == "Male" and age >= 50:

        st.write(
            "✅ Prostate Screening"
        )

    if age < 40:

        st.write(
            "✅ Annual General Health Check-Up"
        )

    st.info(
        "This assessment is intended for educational and preventive healthcare purposes only and is not a medical diagnosis."
    )