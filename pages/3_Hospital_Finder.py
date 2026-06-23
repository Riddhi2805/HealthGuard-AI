import streamlit as st
import requests
import pandas as pd

st.title("🏥 Hospital Finder")

st.write(
    "Search for hospitals near your location."
)

PROFILE_FILE = "data/user_profile.csv"

try:
    profile_df = pd.read_csv(
        PROFILE_FILE
    )
except:
    profile_df = pd.DataFrame()

current_email = st.session_state.get(
    "email"
)

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

location = st.text_input(
    "Enter Area / City",
    placeholder="Airoli, Navi Mumbai"
)
st.caption(
    "Tip: Use area and city together, e.g., Dadar,Mumbai/Airoli Navi,Mumbai/Thane,Mumbai."
)
if st.button("Find Hospitals"):

    if not location.strip():

        st.warning(
            "Please enter an area or city."
        )

    else:

        query = f"hospitals in {location}"

        url = "https://nominatim.openstreetmap.org/search"

        params = {
            "q": query,
            "format": "json",
            "limit": 10
        }

        headers = {
            "User-Agent": "HealthGuardAI"
        }

        response = requests.get(
            url,
            params=params,
            headers=headers,
            timeout=10
        )

        try:

            data = response.json()

        except:

            st.error(
                "Unable to fetch hospital data. Please try again."
            )

            st.stop()

        if data:

            st.success(
                f"Found {len(data)} results"
            )

            for i, hospital in enumerate(
                data,
                start=1
            ):

                name = hospital[
                    "display_name"
                ].split(",")[0]

                st.subheader(
                    f"{i}. 🏥 {name}"
                )

                st.write(
                    f"📍 {hospital['display_name']}"
                )

                lat = hospital["lat"]
                lon = hospital["lon"]

                maps_url = (
                    f"https://www.google.com/maps/search/?api=1&query={lat},{lon}"
                )

                st.link_button(
                    "📍 Open in Google Maps",
                    maps_url
                )

                st.markdown("---")

        else:

            st.warning(
                "No hospitals found."
            )
