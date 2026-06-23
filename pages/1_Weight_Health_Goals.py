import streamlit as st
import pandas as pd
from datetime import date, datetime, timedelta

# ==================================================
# PART 1 - BMI CALCULATOR
# ==================================================

st.title("⚖️ Weight & Health Goals")

st.write(
    "Track your BMI, set health goals, monitor progress, and earn rewards for achieving milestones."
)


PROFILE_FILE = "data/user_profile.csv"

current_email = st.session_state.get(
    "email"
)

try:

    profile_df = pd.read_csv(
        PROFILE_FILE
    )

except:

    profile_df = pd.DataFrame()

if current_email and not profile_df.empty:

    profile_df = profile_df[
        profile_df["Email"]
        ==
        current_email
    ]

# Sidebar

st.sidebar.title(
    "🏥 HealthGuard AI"
)


if current_email and not profile_df.empty:

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

if current_email and not profile_df.empty:

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

    profile_exists = True

else:

    default_gender = "Select"

    default_age = 25

    default_height = 170.0

    default_weight = 70.0

    profile_exists = False


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
    disabled=False
)


age = st.number_input(
    "Age",
    min_value=1,
    max_value=120,
    value=default_age,
    disabled=False
)

height = st.number_input(
    "Height (cm)",
    min_value=50.0,
    max_value=250.0,
    value=default_height,
    disabled=False
)

weight = st.number_input(
    "Weight (kg)",
    min_value=10.0,
    max_value=300.0,
    value=default_weight,
    disabled=False
)

# --------------------------------------------------
# BMI CALCULATION
# --------------------------------------------------

if st.button("Calculate BMI"):

    if gender == "Select":
        st.warning(
        "Please select a gender."
        )
        st.stop()

    height_m = height / 100

    bmi = weight / (height_m ** 2)

    ideal_min = 18.5 * (height_m ** 2)

    ideal_max = 24.9 * (height_m ** 2)

    st.subheader(
        f"Your BMI: {bmi:.2f}"
    )

    st.info(
        f"Ideal Weight Range: {ideal_min:.1f} kg - {ideal_max:.1f} kg"
    )

    # --------------------------------------------------
    # BMI CATEGORY
    # --------------------------------------------------
    
    if bmi < 18.5:

        category = "Underweight"

        st.warning(
            "Underweight"
        )

        needed = ideal_min - weight

        st.write(
            f"You may need approximately {needed:.1f} kg to reach the healthy weight range."
        )

        st.subheader(
            "🥗 Recommendations"
        )

        st.write(
            "• Increase healthy calorie intake"
        )

        st.write(
            "• Include protein-rich foods"
        )

        st.write(
            "• Eat frequent balanced meals"
        )

        st.write(
            "• Focus on strength training"
        )

    elif bmi < 25:

        category = "Normal Weight"

        st.success(
            "Normal Weight"
        )

        st.subheader(
            "✅ Recommendations"
        )

        st.write(
            "• Maintain balanced nutrition"
        )

        st.write(
            "• Stay physically active"
        )

        st.write(
            "• Continue healthy habits"
        )

    elif bmi < 30:

        category = "Overweight"

        st.warning(
            "Overweight"
        )

        excess = weight - ideal_max

        st.write(
            f"You are approximately {excess:.1f} kg above the recommended range."
        )

        st.subheader(
            "🏃 Recommendations"
        )

        st.write(
            "• Increase physical activity"
        )

        st.write(
            "• Reduce sugary drinks"
        )

        st.write(
            "• Increase protein and fiber intake"
        )

        st.write(
            "• Improve sleep quality"
        )

    else:

        category = "Obese"

        st.error(
            "Obese"
        )

        st.subheader(
            "⚕ Recommendations"
        )

        st.write(
            "• Consult a healthcare professional"
        )

        st.write(
            "• Follow a structured weight management plan"
        )

        st.write(
            "• Increase activity gradually"
        )

        st.write(
            "• Track progress regularly"
        )

    # --------------------------------------------------
    # SAVE BMI VALUES
    # --------------------------------------------------

    st.session_state["bmi"] = bmi

    st.session_state["weight"] = weight

    st.session_state["category"] = category

    st.session_state["height"] = height


# ==================================================
# PART 2 - HEALTH GOAL
# ==================================================

st.divider()

if profile_exists:
    st.header("🎯 Health Goal")
    GOALS_FILE = "data/bmi_goals.csv"
    PROGRESS_FILE = "data/bmi_progress.csv"

    # --------------------------------------------------
    # LOAD GOALS
    # --------------------------------------------------

    try:
        goals_df = pd.read_csv(
        GOALS_FILE
    )
    except:
        goals_df = pd.DataFrame()

    
    if current_email and not goals_df.empty:

        goals_df = goals_df[
            goals_df["Email"]
            ==
            current_email
        ]

    active_goal_exists = False

    if not goals_df.empty:

        active_goal_exists = (
            goals_df["Status"]
            ==
            "Active"
        ).any()


    # --------------------------------------------------
    # CREATE GOAL
    # --------------------------------------------------

    if active_goal_exists:

        st.warning(
            "You already have an active goal. Complete it before creating a new one."
        )

    else:

        current_weight = st.session_state.get(
            "weight",
            float(profile["Weight"])
        )

        st.subheader(
            "Create New Goal"
        )

        start_weight = current_weight

        st.write(
            f"Current Weight: {start_weight:.1f} kg"
        )

        target_weight = st.number_input(
            "Target Weight (kg)",
            min_value=10.0,
            max_value=300.0,
            value=float(start_weight)
        )

        from datetime import date, timedelta

        start_date = date.today()

        st.write(
            f"📅 Goal Start Date: {start_date}"
        )

        target_date = st.date_input(
            "Target Completion Date",
            min_value=date.today() + timedelta(days=1),
            value=date.today() + timedelta(days=30)
        )

        # --------------------------------------------------
        # VALIDATION
        # --------------------------------------------------

        if target_weight == start_weight:

            st.info(
                "Enter a target weight different from your current weight."
            )

        else:

            if st.button(
                "🎯 Create Goal"
            ):
                try:

                    all_goals = pd.read_csv(
                        GOALS_FILE
                    )

                except:

                    all_goals = pd.DataFrame()

                if all_goals.empty:

                    goal_id = 1

                else:

                    goal_id = int(
                        all_goals["GoalID"].max()
                    ) + 1

                new_goal = pd.DataFrame(
                    [[
                        current_email,
                        goal_id,
                        date.today(),
                        start_date,
                        target_date,
                        start_weight,
                        target_weight,
                        "Active"
                    ]],
                    columns=[
                        "Email",
                        "GoalID",
                        "CreatedDate",
                        "StartDate",
                        "TargetDate",
                        "StartWeight",
                        "TargetWeight",
                        "Status"
                    ]
                )

                new_goal.to_csv(
                    GOALS_FILE,
                    mode="a",
                    header=not pd.io.common.file_exists(GOALS_FILE),
                    index=False
                )

                st.success(
                    "🎉 Health Goal Created Successfully!"
                )

                st.rerun()
    # ==================================================
    # PART 3 - PROGRESS DASHBOARD
    # ==================================================

    st.divider()

    st.header("📈 Progress Dashboard")

    try:
        goals_df = pd.read_csv(
        GOALS_FILE
    )
    except:
        goals_df = pd.DataFrame()
    
    if current_email and not goals_df.empty:

        goals_df = goals_df[
            goals_df["Email"]
            ==
            current_email
        ]

    try:
        progress_df = pd.read_csv(
            PROGRESS_FILE
        )
    except:
        progress_df = pd.DataFrame(
            columns=[
                "Email",
                "GoalID",
                "Date",
                "Weight"
            ]
        )

    active_goal = None

    if not goals_df.empty:

        active_goals = goals_df[
            goals_df["Status"] == "Active"
        ]

        if not active_goals.empty:

            active_goal = active_goals.iloc[-1]

    # --------------------------------------------------
    # ACTIVE GOAL
    # --------------------------------------------------

    if active_goal is not None:

        goal_id = int(
            active_goal["GoalID"]
        )

        start_weight = float(
            active_goal["StartWeight"]
        )

        target_weight = float(
            active_goal["TargetWeight"]
        )

        start_date = pd.to_datetime(
            active_goal["StartDate"]
        )

        target_date = pd.to_datetime(
            active_goal["TargetDate"]
        )

        goal_progress = progress_df[
            (progress_df["GoalID"] == goal_id)
            &
            (progress_df["Email"] == current_email)
        ]

        # ----------------------------------------------
        # CURRENT WEIGHT
        # ----------------------------------------------

        if goal_progress.empty:

            current_weight = start_weight

        else:

            current_weight = float(
                goal_progress.iloc[-1]["Weight"]
            )

        # ----------------------------------------------
        # UPDATE PROGRESS
        # ----------------------------------------------

        st.subheader(
            "⚖ Update Weight Progress"
        )

        updated_weight = st.number_input(
            "Current Weight Today (kg)",
            min_value=10.0,
            max_value=300.0,
            value=float(current_weight),
            key="update_weight"
        )

        if st.button(
            "📈 Update Progress"
        ):

            new_progress = pd.DataFrame(
                [[
                    current_email,
                    goal_id,
                    datetime.now().strftime(
                        "%Y-%m-%d"
                    ),
                    updated_weight
                ]],
                columns=[
                    "Email",
                    "GoalID",
                    "Date",
                    "Weight"
                ]
            )

            new_progress.to_csv(
                PROGRESS_FILE,
                mode="a",
                header=False,
                index=False
            )

            # ----------------------------------------------
            # UPDATE PROFILE WEIGHT
            # ----------------------------------------------

            all_profiles = pd.read_csv(
                PROFILE_FILE
            )

            all_profiles.loc[
                all_profiles["Email"]
                ==
                current_email,
                "Weight"
            ] = updated_weight

            all_profiles.to_csv(
                PROFILE_FILE,
                index=False
            )

            st.success(
                f"Progress updated successfully! Current profile weight updated to {updated_weight:.1f} kg."
            )

            st.rerun()

        st.divider()

        # ----------------------------------------------
        # CALCULATIONS
        # ----------------------------------------------

        total_change_needed = abs(
            start_weight - target_weight
        )

        achieved_change = abs(
            start_weight - current_weight
        )

        weight_remaining = abs(
            current_weight - target_weight
        )

        if total_change_needed > 0:

            progress_percent = min(
                (
                    achieved_change
                    / total_change_needed
                ) * 100,
                100
            )

        else:

            progress_percent = 0

        # ----------------------------------------------
        # METRICS
        # ----------------------------------------------

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Start Weight",
            f"{start_weight:.1f} kg"
        )

        col2.metric(
            "Current Weight",
            f"{current_weight:.1f} kg"
        )

        col3.metric(
            "Target Weight",
            f"{target_weight:.1f} kg"
        )

        col4.metric(
            "Remaining",
            f"{weight_remaining:.1f} kg"
        )

        st.progress(
            progress_percent / 100
        )

        st.write(
            f"### Progress Towards Goal: {progress_percent:.1f}%"
        )

        # ----------------------------------------------
        # DAYS REMAINING
        # ----------------------------------------------

        today = pd.Timestamp.today()

        total_days = (
            target_date - start_date
        ).days

        days_passed = (
            today - start_date
        ).days

        days_remaining = max(
            (
                target_date - today
            ).days,
            0
        )

        st.info(
            f"📅 Days Remaining: {days_remaining}"
        )

        # ----------------------------------------------
        # STATUS
        # ----------------------------------------------

        if total_days > 0:

            expected_progress = (
                days_passed / total_days
            )

        else:

            expected_progress = 1

        actual_progress = (
            progress_percent / 100
        )

        if actual_progress > expected_progress + 0.10:

            st.success(
                "🟢 Ahead of Schedule"
            )

        elif actual_progress < expected_progress - 0.10:

            st.error(
                "🔴 Behind Schedule"
            )

        else:

            st.warning(
                "🟡 On Track"
            )

        # ----------------------------------------------
        # HISTORY
        # ----------------------------------------------

        st.divider()

        st.subheader(
            "📋 Weight Update History"
        )

        if not goal_progress.empty:

            st.dataframe(
                goal_progress.sort_values(
                    "Date",
                    ascending=False
                ),
                use_container_width=True
            )

            st.subheader(
                "📈 Weight Trend"
            )

            chart_df = goal_progress.copy()

            chart_df["Date"] = pd.to_datetime(
                chart_df["Date"]
            )

            chart_df = chart_df.sort_values(
                "Date"
            )

            st.line_chart(
                chart_df.set_index(
                    "Date"
                )["Weight"]
            )

        else:

            st.info(
                "No progress updates yet."
            )
            
        # ----------------------------------------------
        # GOAL COMPLETION
        # ----------------------------------------------

        goal_completed = False

        # Weight loss goal

        if target_weight < start_weight:

            if current_weight <= target_weight:

                goal_completed = True

        # Weight gain goal

        elif target_weight > start_weight:

            if current_weight >= target_weight:

                goal_completed = True

        if goal_completed:

            try:

                rewards_df = pd.read_csv(
                    "data/rewards.csv"
                )

            except:

                rewards_df = pd.DataFrame()

            already_rewarded = False

            if not rewards_df.empty:

                already_rewarded = (
                    (
                        rewards_df["Email"]
                        ==
                        current_email
                    )
                    &
                    (
                        rewards_df["Activity"]
                        ==
                        "BMI Goal Completed"
                    )
                ).any()

            st.success(
                "🏆 Goal Achieved!"
            )

            if not already_rewarded:

                st.success(
                    "🎁 Reward Granted: +100 Points added to your account!"
                )
            

            if days_remaining > 0:

                st.success(
                    "🟢 Achieved Ahead of Schedule"
                )

            all_goals = pd.read_csv(
                GOALS_FILE
            )

            all_goals.loc[
                (all_goals["GoalID"] == goal_id)
                &
                (all_goals["Email"] == current_email),
                "Status"
            ] = "Completed"

            # ----------------------------------------------
            # BMI REWARD
            # ----------------------------------------------
            if not already_rewarded:
                reward_entry = pd.DataFrame(
                    [[
                        current_email,
                        datetime.now().strftime("%Y-%m-%d"),
                        "BMI Goal Completed",
                        100
                    ]],
                    columns=[
                        "Email",
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

            all_goals.to_csv(
                GOALS_FILE,
                index=False
            )

            st.balloons()
            
            
    else:

        st.info(
            "No active goal found."
        )

else:

    st.info(
        "🔓 Create a profile to unlock Health Goals, Progress Tracking, Rewards, and Personalized Health Insights."
    )