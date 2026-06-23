import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="HealthGuard AI",
    page_icon="🏥",
    layout="wide"
)

# ==================================================
# SESSION
# ==================================================

current_email = st.session_state.get(
    "email"
)

# ==================================================
# FILES
# ==================================================

PROFILE_FILE = "data/user_profile.csv"
GOALS_FILE = "data/bmi_goals.csv"
REMINDER_FILE = "data/reminders.csv"
REWARDS_FILE = "data/rewards.csv"

# ==================================================
# LOAD DATA
# ==================================================

try:

    profile_df = pd.read_csv(
        PROFILE_FILE
    )

except:

    profile_df = pd.DataFrame()

try:

    goals_df = pd.read_csv(
        GOALS_FILE
    )

except:

    goals_df = pd.DataFrame()

try:

    reminders_df = pd.read_csv(
        REMINDER_FILE
    )

except:

    reminders_df = pd.DataFrame()

try:

    rewards_df = pd.read_csv(
        REWARDS_FILE
    )

except:

    rewards_df = pd.DataFrame()

# ==================================================
# FILTER CURRENT USER
# ==================================================

if current_email:

    if not profile_df.empty:

        profile_df = profile_df[
            profile_df["Email"]
            ==
            current_email
        ]

else:

    profile_df = pd.DataFrame()

profile_exists = not profile_df.empty

if current_email:

    if not goals_df.empty:

        goals_df = goals_df[
            goals_df["Email"]
            ==
            current_email
        ]

    if not reminders_df.empty:

        reminders_df = reminders_df[
            reminders_df["Email"]
            ==
            current_email
        ]

    if not rewards_df.empty:

        rewards_df = rewards_df[
            rewards_df["Email"]
            ==
            current_email
        ]

else:

    goals_df = pd.DataFrame()

    reminders_df = pd.DataFrame()

    rewards_df = pd.DataFrame()

# ==================================================
# SIDEBAR
# ==================================================

st.sidebar.title(
    "🏥 HealthGuard AI"
)

if profile_exists:

    profile = profile_df.iloc[0]

    st.sidebar.success(
        f"👋 Welcome, {profile['Name']}!"
    )

else:

    st.sidebar.success(
        "👋 Welcome, User!"
    )

st.sidebar.markdown("---")

st.sidebar.caption(
    "Empowering Preventive Healthcare Through AI"
)

# ==================================================
# PAGE HEADER
# ==================================================

st.title("🏥 HealthGuard AI")

st.subheader(
    "Your Preventive Healthcare Companion"
)

st.markdown("---")

# ==================================================
# WELCOME SECTION
# ==================================================

if profile_exists:

    profile = profile_df.iloc[0]

    st.success(
        f"👋 Welcome back, {profile['Name']}!"
    )

else:

    st.info(
        """
        Welcome to HealthGuard AI.

        You can use:

        ✅ BMI Calculator
        ✅ Health Risk Assessment
        ✅ Hospital Finder
        ✅ Healthcare Cost Checker
        ✅ AI Medical Report Analyzer

        Login and create a profile to unlock:

        🎯 Weight Goals

        🔔 Health Reminders

        🏆 Rewards & Badges

        📊 Personalized Health Tracking
        """
    )

st.markdown("---")
# ==================================================
# QUICK HEALTH DASHBOARD
# ==================================================

st.header("📊 Quick Health Dashboard")

if profile_exists:

    total_points = 0

    if not rewards_df.empty:

        total_points = rewards_df["Points"].sum()

    active_goals = 0

    if not goals_df.empty:

        active_goals = len(
            goals_df[
                goals_df["Status"]
                ==
                "Active"
            ]
        )

    pending_reminders = 0

    if not reminders_df.empty:

        pending_reminders = len(
            reminders_df[
                reminders_df["Status"]
                ==
                "Pending"
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
        "🎯 Active Goals",
        active_goals
    )

else:

    st.info(
        "Login and create a profile to view your personalized dashboard."
    )

st.markdown("---")

# ==================================================
# HEALTH SUMMARY
# ==================================================

st.header("📋 Health Summary")

if profile_exists:

    if not goals_df.empty:

        active_goals_df = goals_df[
            goals_df["Status"]
            ==
            "Active"
        ]

        if not active_goals_df.empty:

            active_goal = (
                active_goals_df.iloc[-1]
            )

            st.info(
                f"🎯 Active Goal: {active_goal['StartWeight']} kg → {active_goal['TargetWeight']} kg"
            )

    if not reminders_df.empty:

        pending_df = reminders_df[
            reminders_df["Status"]
            ==
            "Pending"
        ]

        if not pending_df.empty:

            next_reminder = (
                pending_df
                .sort_values(
                    "Reminder Date"
                )
                .iloc[0]
            )

            st.warning(
                f"🔔 Next Reminder: {next_reminder['Title']} ({next_reminder['Reminder Date']})"
            )

    if not rewards_df.empty:

        latest_reward = rewards_df.iloc[-1]

        st.success(
            f"🏆 Latest Reward: {latest_reward['Activity']} (+{latest_reward['Points']} Points)"
        )

else:

    st.info(
        "No personalized health summary available."
    )

st.markdown("---")

# ==================================================
# AVAILABLE FEATURES
# ==================================================

st.header("🚀 Available Features")

col1, col2, col3 = st.columns(3)

with col1:

    st.success(
        "⚖️ BMI Calculator"
    )

    st.success(
        "🩺 Health Risk Assessment"
    )

with col2:

    st.success(
        "🏥 Hospital Finder"
    )

    st.success(
        "💰 Healthcare Cost Checker"
    )

with col3:

    st.success(
        "🤖 AI Medical Report Analyzer"
    )

    st.success(
        "🔔 Health Reminders"
    )

    st.success(
        "🎯 Weight Goals"
    )

    st.success(
        "🏆 Rewards & Badges"
    )

st.markdown("---")

# ==================================================
# HEALTH TIP
# ==================================================

tips = [

    "Drink enough water every day.",

    "Regular exercise improves overall health.",

    "Annual health checkups help detect risks early.",

    "Sleep is essential for physical and mental well-being.",

    "Preventive healthcare is often less expensive than treatment."
]

st.header(
    "💡 Health Tip of the Day"
)

st.info(
    random.choice(tips)
)

st.info(
    "Did You Know? Many chronic diseases can be managed more effectively when detected early through routine health screenings."
)