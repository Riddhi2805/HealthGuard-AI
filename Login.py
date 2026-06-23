import streamlit as st
import pandas as pd
import re
import hashlib
from datetime import date

st.set_page_config(
    page_title="HealthGuard AI Account",
    page_icon="🏥"
)

USERS_FILE = "data/users.csv"
PROFILE_FILE = "data/user_profile.csv"

# ======================================
# LOAD USERS
# ======================================

try:

    users_df = pd.read_csv(
        USERS_FILE
    )

except:

    users_df = pd.DataFrame(
        columns=[
            "Email",
            "Password"
        ]
    )

# ======================================
# LOAD PROFILES
# ======================================

try:

    profile_df = pd.read_csv(
        PROFILE_FILE
    )

except:

    profile_df = pd.DataFrame(
        columns=[
            "Email",
            "Name",
            "DOB",
            "Gender",
            "Height",
            "Weight"
        ]
    )

# ======================================
# PAGE TITLE
# ======================================

st.title("🏥 HealthGuard AI")

# ======================================
# NOT LOGGED IN
# ======================================

if not st.session_state.get(
    "logged_in",
    False
):

    st.subheader(
        "Secure Login & Registration"
    )

    tab1, tab2 = st.tabs(
        [
            "🔐 Login",
            "📝 Register"
        ]
    )

    # ==================================
    # REGISTER
    # ==================================

    with tab2:

        st.header(
            "Create New Account"
        )

        reg_email = st.text_input(
            "Email Address",
            key="reg_email"
        )

        reg_password = st.text_input(
            "Password",
            type="password",
            key="reg_password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            key="reg_confirm"
        )

        st.caption(
            "Password must contain at least 8 characters, one uppercase letter, one lowercase letter, and one number."
        )

        if st.button(
            "📝 Register",
            key="register_btn"
        ):

            if not reg_email.strip():

                st.warning(
                    "Please enter an email."
                )

            elif reg_email in users_df["Email"].values:

                st.warning(
                    "Email already registered."
                )

            elif reg_password != confirm_password:

                st.warning(
                    "Passwords do not match."
                )

            elif len(reg_password) < 8:

                st.warning(
                    "Password must be at least 8 characters long."
                )

            elif not re.search(
                r"[A-Z]",
                reg_password
            ):

                st.warning(
                    "Password must contain at least one uppercase letter."
                )

            elif not re.search(
                r"[a-z]",
                reg_password
            ):

                st.warning(
                    "Password must contain at least one lowercase letter."
                )

            elif not re.search(
                r"\d",
                reg_password
            ):

                st.warning(
                    "Password must contain at least one number."
                )

            else:

                hashed_password = hashlib.sha256(
                    reg_password.encode()
                ).hexdigest()

                new_user = pd.DataFrame(
                    [[
                        reg_email,
                        hashed_password
                    ]],
                    columns=[
                        "Email",
                        "Password"
                    ]
                )

                users_df = pd.concat(
                    [
                        users_df,
                        new_user
                    ],
                    ignore_index=True
                )

                users_df.to_csv(
                    USERS_FILE,
                    index=False
                )

                st.success(
                    "✅ Registration Successful!"
                )

                st.rerun()

    # ==================================
    # LOGIN
    # ==================================

    with tab1:

        st.header(
            "Login"
        )

        login_email = st.text_input(
            "Email",
            key="login_email"
        )

        login_password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "🔐 Login",
            key="login_btn"
        ):
            hashed_login_password = hashlib.sha256(
                login_password.encode()
            ).hexdigest()

            user = users_df[
                (users_df["Email"] == login_email)
                &
                (users_df["Password"] == hashed_login_password)
            ]

            if not user.empty:

                st.session_state[
                    "logged_in"
                ] = True

                st.session_state[
                    "email"
                ] = login_email

                st.success(
                    "✅ Login Successful!"
                )

                st.rerun()

            else:

                st.error(
                    "❌ Invalid Email or Password."
                )

# ======================================
# LOGGED IN ACCOUNT PAGE
# ======================================

else:

    current_email = st.session_state[
        "email"
    ]

    st.subheader(
        "👤 My Account"
    )

    st.success(
        f"Logged in as {current_email}"
    )

    user_profile = profile_df[
        profile_df["Email"]
        ==
        current_email
    ]

    # ==================================
    # PROFILE NOT CREATED
    # ==================================

    if user_profile.empty:

        st.warning(
            "Please complete your profile."
        )

        name = st.text_input(
            "Name",
            key="create_name"
        )

        dob = st.date_input(
            "Date of Birth",
            value=date(2000, 1, 1),
            min_value=date(1900, 1, 1),
            max_value=date.today(),
            key="create_dob"
        )

        gender = st.selectbox(
            "Gender",
            [
                "Male",
                "Female",
                "Other"
            ],
            key="create_gender"
        )

        height = st.number_input(
            "Height (cm)",
            min_value=50.0,
            max_value=250.0,
            key="create_height"
        )

        weight = st.number_input(
            "Weight (kg)",
            min_value=10.0,
            max_value=300.0,
            key="create_weight"
        )
        

        if st.button(
            "💾 Save Profile"
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

            if age < 1:

                st.warning(
                    "⚠️ Please enter a valid Date of Birth."
                )

                st.stop()

            elif not name.strip():

                st.warning(
                    "⚠️ Please enter your name."
                )

            else:
                new_profile = pd.DataFrame(
                    [[
                        current_email,
                        name,
                        dob,
                        gender,
                        height,
                        weight
                    ]],
                    columns=[
                        "Email",
                        "Name",
                        "DOB",
                        "Gender",
                        "Height",
                        "Weight"
                    ]
                )

                profile_df = pd.concat(
                    [
                        profile_df,
                        new_profile
                    ],
                    ignore_index=True
                )

                profile_df.to_csv(
                    PROFILE_FILE,
                    index=False
                )

                st.success(
                    "Profile saved successfully."
                )

                st.rerun()

    # ==================================
    # PROFILE EXISTS
    # ==================================

    else:

        profile = user_profile.iloc[0]


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


        col1, col2 = st.columns(2)

        col1.metric(
            "Age",
            age
        )

        col2.metric(
            "Gender",
            profile["Gender"]
        )

        col1, col2 = st.columns(2)

        col1.metric(
            "Height",
            f"{profile['Height']} cm"
        )

        col2.metric(
            "Weight",
            f"{profile['Weight']} kg"
        )

        with st.expander(
            "✏️ Edit Profile"
        ):

            name = st.text_input(
                "Name",
                value=profile["Name"],
                key="edit_name"
            )

            dob = st.date_input(
                "Date of Birth",
                value=pd.to_datetime(
                    profile["DOB"]
                ).date(),
                min_value=date(1900, 1, 1),
                max_value=date.today(),
                key="edit_dob"
            )

            gender = st.selectbox(
                "Gender",
                [
                    "Male",
                    "Female",
                    "Other"
                ],
                index=[
                    "Male",
                    "Female",
                    "Other"
                ].index(
                    profile["Gender"]
                ),
                key="edit_gender"
            )

            height = st.number_input(
                "Height (cm)",
                min_value=50.0,
                max_value=250.0,
                value=float(
                    profile["Height"]
                ),
                key="edit_height"
            )

            weight = st.number_input(
                "Weight (kg)",
                min_value=10.0,
                max_value=300.0,
                value=float(
                    profile["Weight"]
                ),
                key="edit_weight"
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

                if age < 1:

                    st.warning(
                        "⚠️ Please enter a valid Date of Birth."
                    )

                    st.stop()

                elif not name.strip():

                    st.warning(
                        "⚠️ Please enter your name."
                    )

                else:
                    profile_df.loc[
                        profile_df["Email"]
                        ==
                        current_email,
                        [
                            "Name",
                            "DOB",
                            "Gender",
                            "Height",
                            "Weight"
                        ]
                    ] = [
                        name,
                        str(dob),
                        gender,
                        height,
                        weight
                    ]

                    profile_df.to_csv(
                        PROFILE_FILE,
                        index=False
                    )

                    st.success(
                        "Profile updated successfully."
                    )
                    st.rerun()

        st.divider()

        if st.button(
            "👤 Delete Profile"
        ):

            profile_df = profile_df[
                profile_df["Email"]
                !=
                current_email
            ]

            profile_df.to_csv(
                PROFILE_FILE,
                index=False
            )

            try:

                goals_df = pd.read_csv(
                    "data/bmi_goals.csv"
                )

                goals_df = goals_df[
                    goals_df["Email"]
                    !=
                    current_email
                ]

                goals_df.to_csv(
                    "data/bmi_goals.csv",
                    index=False
                )

            except:
                pass

            try:

                reminders_df = pd.read_csv(
                    "data/reminders.csv"
                )

                reminders_df = reminders_df[
                    reminders_df["Email"]
                    !=
                    current_email
                ]

                reminders_df.to_csv(
                    "data/reminders.csv",
                    index=False
                )

            except:
                pass

            try:

                rewards_df = pd.read_csv(
                    "data/rewards.csv"
                )

                rewards_df = rewards_df[
                    rewards_df["Email"]
                    !=
                    current_email
                ]

                rewards_df.to_csv(
                    "data/rewards.csv",
                    index=False
                )

            except:
                pass

            st.success(
                "Profile deleted successfully."
            )

            st.rerun()

    st.divider()

    if st.button(
        "🚪 Logout"
    ):

        st.session_state.clear()

        st.rerun()

    confirm_delete = st.checkbox(
        "I understand this action cannot be undone."
    )

    if st.button(
        "🗑️ Delete Account"
    ) and confirm_delete:

        users_df = users_df[
            users_df["Email"]
            !=
            current_email
        ]

        users_df.to_csv(
            USERS_FILE,
            index=False
        )

        profile_df = profile_df[
            profile_df["Email"]
            !=
            current_email
        ]

        profile_df.to_csv(
            PROFILE_FILE,
            index=False
        )

        st.session_state.clear()

        st.success(
            "Account deleted successfully."
        )

        st.rerun()