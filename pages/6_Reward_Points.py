import streamlit as st
import pandas as pd

REWARDS_FILE = "data/rewards.csv"

st.title("🏆 Reward Points")

st.write(
    "Earn points by completing health goals and preventive health checkups."
)

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

if profile_df.empty:

    st.info(
        "🔓 Create a profile to unlock Rewards, Health Tracking, Goals, and Personalized Insights."
    )

    st.stop()

# ==================================================
# PART 1 - REWARD DASHBOARD
# ==================================================

st.header("📊 Reward Dashboard")

try:

    rewards_df = pd.read_csv(
        REWARDS_FILE
    )

except:

    rewards_df = pd.DataFrame(
        columns=[
            "Date",
            "Activity",
            "Points"
        ]
    )

if rewards_df.empty:

    st.info(
        "No rewards earned yet."
    )

else:

    total_points = rewards_df[
        "Points"
    ].sum()

    total_activities = len(
        rewards_df
    )

    bmi_points = rewards_df[
        rewards_df["Activity"] == "BMI Goal Completed"
    ]["Points"].sum()

    reminder_points = rewards_df[
        rewards_df["Activity"].str.contains(
            "Completed",
            case=False,
            na=False
        )
    ]["Points"].sum() - bmi_points

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🏆 Total Points",
        int(total_points)
    )

    col2.metric(
        "📈 Activities",
        total_activities
    )

    col3.metric(
        "⚖️ BMI Rewards",
        int(bmi_points)
    )

    col4.metric(
        "🔔 Reminder Rewards",
        int(reminder_points)
    )

# ==================================================
# PART 2 - REWARD HISTORY
# ==================================================

st.divider()

st.header("📋 Reward History")

if rewards_df.empty:

    st.info(
        "No reward history available."
    )

else:

    history_df = rewards_df.copy()

    history_df = history_df.sort_values(
        "Date",
        ascending=False
    )

    st.dataframe(
        history_df,
        use_container_width=True
    )

# ----------------------------------------------
# TOTAL POINTS
# ----------------------------------------------

if rewards_df.empty:

    total_points = 0

else:

    total_points = rewards_df["Points"].sum()


# ==================================================
# PART 3 - ACHIEVEMENT BADGE
# ==================================================

st.divider()

st.header("🏅 Achievement Badge")

if total_points < 100:

    badge = "🥉 Bronze Health Explorer"

elif total_points < 300:

    badge = "🥈 Silver Health Champion"

elif total_points < 500:

    badge = "🥇 Gold Wellness Master"

else:

    badge = "💎 Platinum Health Legend"

st.success(
    f"Current Badge: {badge}"
)

if total_points < 100:

    st.progress(
        total_points / 100
    )

    st.caption(
        f"{100-total_points} points to Silver Health Champion"
    )

elif total_points < 300:

    st.progress(
        (total_points - 100) / 200
    )

    st.caption(
        f"{300-total_points} points to Gold Wellness Master"
    )

elif total_points < 500:

    st.progress(
        (total_points - 300) / 200
    )

    st.caption(
        f"{500-total_points} points to Platinum Health Legend"
    )

else:

    badge = "💎 Platinum Health Legend"

    st.balloons()

    st.caption(
        "🎉 Congratulations! You have reached the highest achievement badge."
    )

# ==================================================
# PART 4 - REWARD ANALYTICS
# ==================================================

st.divider()

st.header("📈 Reward Analytics")

if not rewards_df.empty:

    # ----------------------------------------------
    # POINTS BY ACTIVITY
    # ----------------------------------------------

    st.subheader(
        "🏆 Points by Activity"
    )

    activity_points = rewards_df.groupby(
        "Activity"
    )["Points"].sum()

    st.bar_chart(
        activity_points
    )

    # ----------------------------------------------
    # POINTS BY DATE
    # ----------------------------------------------

    st.subheader(
        "📅 Points Earned by Date"
    )

    daily_points = rewards_df.groupby(
        "Date"
    )["Points"].sum()

    st.bar_chart(
        daily_points
    )
