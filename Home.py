import streamlit as st
import random
import pandas as pd
import random
from datetime import date

st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🏥",
    layout="wide"
)

PROFILE_FILE = "data/user_profile.csv"
GOALS_FILE = "data/bmi_goals.csv"
REMINDER_FILE = "data/reminders.csv"
REWARDS_FILE = "data/rewards.csv"

try:

    profile_df = pd.read_csv(
        PROFILE_FILE
    )

except:

    profile_df = pd.DataFrame()

try:
    goals_df = pd.read_csv(GOALS_FILE)
except:
    goals_df = pd.DataFrame()

try:
    reminders_df = pd.read_csv(REMINDER_FILE)
except:
    reminders_df = pd.DataFrame()

try:
    rewards_df = pd.read_csv(REWARDS_FILE)
except:
    rewards_df = pd.DataFrame()

if profile_df.empty:

    profile_exists = False

else:

    profile_exists = True


# Sidebar

st.sidebar.title(
    "🏥 HealthGuard AI"
)

if profile_exists:

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

# Main Page
st.title("🏥 HealthGuard AI")
st.subheader("Your Preventive Healthcare Companion")

st.markdown("---")

st.header("👤 User Profile")


if not profile_exists:

    name = st.text_input(
        "Name"
    )

    dob = st.date_input(
        "Date of Birth",
        min_value=date(1900, 1, 1),
        max_value=date.today()
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"]
    )

    height = st.number_input(
        "Height (cm)",
        min_value=50.0,
        max_value=250.0
    )

    weight = st.number_input(
        "Weight (kg)",
        min_value=10.0,
        max_value=300.0
    )

    if st.button("💾 Save Profile"):

        today = date.today()

        age = (
            today.year
            - dob.year
            - (
                (today.month, today.day)
                <
                (dob.month, dob.day)
            )
        )

        if not name.strip():

            st.warning(
                "⚠️ Please enter your name."
            )

        elif age < 1:

            st.warning(
                "⚠️ Please enter a valid Date of Birth."
            )

        else:

            pd.DataFrame(
                [[
                    name,
                    dob,
                    gender,
                    height,
                    weight
                ]],
                columns=[
                    "Name",
                    "DOB",
                    "Gender",
                    "Height",
                    "Weight"
                ]
            ).to_csv(
                PROFILE_FILE,
                index=False
            )

            st.success(
                "✅ Profile saved successfully!"
            )

            

       
            
else:

    profile = profile_df.iloc[0]
    

    dob = pd.to_datetime(
    profile["DOB"]
    ).date()

    today = date.today()

    age = (
        today.year
        - dob.year
        - (
            (today.month, today.day)
            <
            (dob.month, dob.day)
        )
    )

    st.success(
        f"👋 Welcome, {str(profile['Name']).title()}!"
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Age",
        age
    )

    col2.metric(
        "Gender",
        profile["Gender"]
    )

    col3.metric(
        "Height",
        f"{profile['Height']} cm"
    )

    col4.metric(
        "Weight",
        f"{profile['Weight']} kg"
    )

    with st.expander(
        "✏️ Edit Profile"
    ):
        st.caption(
            "Update your personal information and health details."
        )

        name = st.text_input(
            "Name",
            value=profile["Name"]
        )

        dob = st.date_input(
            "Date of Birth",
            value=pd.to_datetime(
                profile["DOB"]
            ).date(),
            min_value=date(1900, 1, 1),
            max_value=date.today()
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"],
            index=[
                "Male",
                "Female",
                "Other"
            ].index(
                profile["Gender"]
            )
        )

        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            value=float(
                profile["Height"]
            )
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=10.0,
            max_value=300.0,
            value=float(
                profile["Weight"]
            )
        )

        if st.button(
            "💾 Update Profile"
            ):

            today = date.today()

            age = (
            today.year
            - dob.year
            - (
            (today.month, today.day)
            <
            (dob.month, dob.day)
            )
            )

            if not name.strip():

                st.warning(
                "⚠️ Please enter your name."
                )

            elif age < 1:

                st.warning(
                "⚠️ Please enter a valid Date of Birth."
                )

            else:

                pd.DataFrame(
                [[
                    name,
                    dob,
                    gender,
                    height,
                    weight
                ]],
                columns=[
                    "Name",
                    "DOB",
                    "Gender",
                    "Height",
                    "Weight"
                ]
                ).to_csv(
                PROFILE_FILE,
                index=False
                )

                st.success(
                "✅ Profile updated successfully!"
                )

                


st.markdown("---")

st.header("📊 Quick Health Dashboard")

if rewards_df.empty:

    total_points = 0

else:

    total_points = rewards_df["Points"].sum()

active_goals = len(
    goals_df[
        goals_df["Status"] == "Active"
    ]
)

pending_reminders = len(
    reminders_df[
        reminders_df["Status"] == "Pending"
    ]
)

if total_points < 100:

    badge = "🥉 Bronze"

elif total_points < 300:

    badge = "🥈 Silver"

elif total_points < 500:

    badge = "🥇 Gold"

else:

    badge = "💎 Platinum"

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "🏆 Total Points",
    total_points
)

col2.metric(
    "🏅 Badge",
    badge
)

col3.metric(
    "🔔 Pending Reminders",
    pending_reminders
)

col4.metric(
    "⚖️ Active Goals",
    active_goals
)

st.markdown("---")

# ==================================================
# HEALTH SUMMARY
# ==================================================

st.header("📋 Health Summary")

# Active Goal

if not goals_df.empty:

    active_goals = goals_df[
        goals_df["Status"] == "Active"
    ]

    if not active_goals.empty:

        active_goal = active_goals.iloc[-1]

        st.info(
            f"🎯 Active Goal: {active_goal['StartWeight']} kg → {active_goal['TargetWeight']} kg"
        )

    else:

        st.info(
            "🎯 No Active Goals"
        )

# Next Reminder

if not reminders_df.empty:

    pending_reminders = reminders_df[
        reminders_df["Status"] == "Pending"
    ]

    if not pending_reminders.empty:

        next_reminder = pending_reminders.sort_values(
            "Reminder Date"
        ).iloc[0]

        st.warning(
            f"🔔 Next Reminder: {next_reminder['Title']} ({next_reminder['Reminder Date']})"
        )

    else:

        st.info(
            "🔔 No Pending Reminders"
        )

# Latest Reward

if not rewards_df.empty:

    latest_reward = rewards_df.iloc[-1]

    st.info(
        f"🏆 Latest Reward: {latest_reward['Activity']} (+{latest_reward['Points']} Points)"
    )

st.markdown("---")

# ==================================================
# AVAILABLE FEATURES
# ==================================================

st.header("🚀 Available Features")

col1, col2, col3 = st.columns(3)

with col1:

    st.success("⚖️ Weight & Health Goals")

    st.success("🩺 Health Risk Assessment")

with col2:

    st.success("🏥 Hospital Finder")

    st.success("💰 Price Comparison")

with col3:

    st.success("🔔 Health Reminders")

    st.success("🏆 Reward Points")



tips = [
    "Drink enough water every day.",
    "Regular exercise improves overall health.",
    "Annual health checkups help detect risks early.",
    "Sleep is essential for physical and mental well-being.",
    "Preventive healthcare is often less expensive than treatment."
]

st.markdown("---")
st.header("💡 Health Tip of the Day")

st.info(random.choice(tips))

st.info(
    "Did You Know? Many chronic diseases can be managed more effectively when detected early through routine health screenings."
)


