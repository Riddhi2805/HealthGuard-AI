import streamlit as st
import pandas as pd
from datetime import date
from datetime import timedelta

REMINDER_FILE = "data/reminders.csv"


st.title("🔔 Health Reminders")

st.write(
    "Create reminders for upcoming health checkups, screenings, and tests."
)

# ==================================================
# PART 1 - CREATE REMINDER
# ==================================================

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
        "🔓 Create a profile to unlock Health Reminders, Health Tracking, Rewards, and Personalized Health Insights."
    )

    st.stop()



st.header("➕ Create New Reminder")

title = st.text_input(
    "Reminder Title"
)

category = st.selectbox(
    "Category",
    [
        "Blood Test",
        "Full Body Checkup",
        "Eye Checkup",
        "Dental Checkup",
        "Vaccination",
        "General Health Checkup",
        "Other"
    ]
)

reminder_date = st.date_input(
    "Reminder Date",
    min_value=date.today() + timedelta(days=1)
)

if st.button("➕ Add Reminder"):

    if title.strip() == "":

        st.error(
            "Please enter a reminder title."
        )

    else:

        try:

            reminders_df = pd.read_csv(
                REMINDER_FILE
            )

        except:

            reminders_df = pd.DataFrame(
                columns=[
                    "Title",
                    "Category",
                    "Reminder Date",
                    "Days Remaining",
                    "Status",
                    "Completed Date",
                    "Reward Given"
                ]
            )

        days_remaining = (
            reminder_date - date.today()
        ).days

        new_reminder = pd.DataFrame(
            [[
                title,
                category,
                reminder_date,
                days_remaining,
                "Pending",
                "",
                "No"
            ]],
            columns=[
                "Title",
                "Category",
                "Reminder Date",
                "Days Remaining",
                "Status",
                "Completed Date",
                "Reward Given"
            ]
        )

        new_reminder.to_csv(
            REMINDER_FILE,
            mode="a",
            header=False,
            index=False
        )

        st.success(
            "Reminder added successfully!"
        )



# ==================================================
# PART 2 - REMINDER DASHBOARD
# ==================================================

st.divider()

st.header("📋 Reminder Dashboard")

try:

    reminders_df = pd.read_csv(
        REMINDER_FILE
    )

except:

    reminders_df = pd.DataFrame(
        columns=[
            "Title",
            "Category",
            "Reminder Date",
            "Days Remaining",
            "Status",
            "Completed Date",
            "Reward Given"
        ]
    )
# ----------------------------------------------
# AUTO EXPIRE AFTER 15 DAYS
# ----------------------------------------------

today = pd.Timestamp.today().date()

for i in reminders_df.index:

    if reminders_df.loc[i, "Status"] == "Pending":

        reminder_date = pd.to_datetime(
            reminders_df.loc[i, "Reminder Date"]
        ).date()

        overdue_days = (
            today - reminder_date
        ).days

        if overdue_days > 16:

            reminders_df.loc[
                i,
                "Status"
            ] = "Not Completed"

reminders_df.to_csv(
    REMINDER_FILE,
    index=False
)

reminders_df["Completed Date"] = (
    reminders_df["Completed Date"]
    .fillna("")
)

if reminders_df.empty:

    st.info(
        "No reminders created yet."
    )

else:

    # ----------------------------------------------
    # UPDATE DAYS REMAINING
    # ----------------------------------------------

    today = pd.Timestamp.today().date()

    for i in reminders_df.index:

        reminder_date = pd.to_datetime(
            reminders_df.loc[
                i,
                "Reminder Date"
            ]
            ).date()

        days_remaining = (
            reminder_date - today
        ).days

        reminders_df.loc[
            i,
            "Days Remaining"
        ] = days_remaining

    reminders_df.to_csv(
        REMINDER_FILE,
        index=False
    )


    # ----------------------------------------------
    # STATUS COUNTERS
    # ----------------------------------------------

    col1, col2, col3 = st.columns(3)

    pending_count = len(
        reminders_df[
            reminders_df["Status"] == "Pending"
        ]
    )

    completed_count = len(
        reminders_df[
            reminders_df["Status"] == "Completed"
        ]
    )

    not_completed_count = len(
        reminders_df[
            reminders_df["Status"] == "Not Completed"
        ]
    )

    col1.metric(
        "Pending",
        pending_count
    )

    col2.metric(
        "Completed",
        completed_count
    )

    col3.metric(
        "Not Completed",
        not_completed_count
    )

    st.divider()

    # ----------------------------------------------
    # REMINDER TABLE
    # ----------------------------------------------

    st.dataframe(
        reminders_df,
        use_container_width=True
    )

# ==================================================
# PART 3 - REMINDER ACTIONS
# ==================================================

st.divider()

st.header("✅ Reminder Actions")

today = pd.Timestamp.today().date()

pending_reminders = reminders_df[
    reminders_df["Status"] == "Pending"
]

action_found = False

for idx, row in pending_reminders.iterrows():

    reminder_date = pd.to_datetime(
        row["Reminder Date"]
    ).date()

    # Only show actions when reminder date arrives

    if reminder_date <= today:

        action_found = True

        st.subheader(
            f"📌 {row['Title']}"
        )

        st.write(
            f"Category: {row['Category']}"
        )

        st.write(
            f"Reminder Date: {row['Reminder Date']}"
        )

        col1, col2 = st.columns(2)

        # ------------------------------------------
        # COMPLETED
        # ------------------------------------------

        if col1.button(
            f"✅ Completed - {idx}"
        ):

            reminders_df.loc[
                idx,
                "Status"
            ] = "Completed"

            reminders_df.loc[
                idx,
                "Completed Date"
            ] = str(today)

            reminders_df.loc[
                idx,
                "Reward Given"
            ] = "Yes"

            reminders_df.to_csv(
                REMINDER_FILE,
                index=False
            )

            # Reward Entry

            reward_entry = pd.DataFrame(
                [[
                    str(today),
                    f"{row['Title']} Completed",
                    50
                ]],
                columns=[
                    "Date",
                    "Activity",
                    "Points"
                ]
            )

            reward_entry.to_csv(
                "data/rewards.csv",
                mode="a",
                header=False,
                index=False
            )

            st.success(
                "Reminder marked as completed! +50 Points"
            )

        # ------------------------------------------
        # NOT COMPLETED
        # ------------------------------------------

        if col2.button(
            f"❌ Not Completed - {idx}"
        ):

            reminders_df.loc[
                idx,
                "Status"
            ] = "Not Completed"

            reminders_df.to_csv(
                REMINDER_FILE,
                index=False
            )

            st.warning(
                "Reminder marked as not completed."
            )

if not action_found:

    st.info(
    "No reminders require action today."
    )
 

