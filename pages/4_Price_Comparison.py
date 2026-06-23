import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE TITLE
# --------------------------------------------------

st.title("💰 Healthcare Cost Checker")

st.write("""
Check whether the amount quoted for a medical test is reasonable
by comparing it with market prices from different providers.
""")

st.divider()

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

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

try:
    df = pd.read_csv("data/treatment_costs.csv")

except Exception:
    st.error("Unable to load treatment cost data.")
    st.stop()

# --------------------------------------------------
# SELECT TEST
# --------------------------------------------------

selected_test = st.selectbox(
    "🧪 Select Medical Test",
    sorted(df["Treatment"].unique())
)
st.caption(
    f"Selected Test: {selected_test}"
)

# --------------------------------------------------
# USER PRICE INPUT
# --------------------------------------------------

user_price = st.number_input(
    "💵 Enter the price you were quoted (₹)",
    min_value=0.0,
    step=50.0
)

st.divider()

# --------------------------------------------------
# FILTER DATA
# --------------------------------------------------

test_data = df[df["Treatment"] == selected_test]

if test_data.empty:
    st.warning("No data available.")
    st.stop()

# --------------------------------------------------
# MARKET STATISTICS
# --------------------------------------------------

avg_price = test_data["Price"].mean()
min_price = test_data["Price"].min()
max_price = test_data["Price"].max()

cheapest_provider = test_data.loc[
    test_data["Price"].idxmin(),
    "Provider"
]

# --------------------------------------------------
# PRICE EVALUATION
# --------------------------------------------------

if user_price > 0:

    difference = user_price - avg_price

    if user_price > avg_price * 1.2:

        assessment = "Overpriced"

        st.subheader(
            f"🤖 Cost Assessment: {assessment}"
        )

        st.warning(
            "📈 Your quoted price is higher than the average market price. Comparing providers may help identify more cost-effective alternatives."
        )

    elif user_price >= avg_price * 0.8:

        assessment = "Fair Price"

        st.subheader(
            f"🤖 Cost Assessment: {assessment}"
        )

        st.info(
            "✅ Your quoted price falls within the typical market range for this test."
        )

    else:

        assessment = "Excellent Value"

        st.subheader(
            f"🤖 Cost Assessment: {assessment}"
        )

        st.success(
            "🎉 Your quoted price is lower than the average market price and appears to offer good value."
        )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Market Average",
            f"₹{avg_price:.0f}"
        )

    with col2:

        st.metric(
            "Your Price",
            f"₹{user_price:.0f}"
        )

    with col3:

        st.metric(
            "Difference",
            f"₹{difference:.0f}",
            f"{((difference / avg_price) * 100):.1f}%"
        )

    with col4:

        st.metric(
            "Price Range",
            f"₹{min_price:.0f} - ₹{max_price:.0f}"
        )

    potential_saving = user_price - min_price

    if potential_saving > 0:

        st.warning(
            f"💰 You could potentially save ₹{potential_saving:.0f} by choosing the lowest-cost provider."
        )

# --------------------------------------------------
# MARKET COMPARISON
# --------------------------------------------------

st.subheader("📊 Market Price Comparison")

comparison_df = test_data[
    ["Provider", "City", "Price"]
].sort_values("Price")

st.dataframe(
    comparison_df,
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# BAR CHART
# --------------------------------------------------

st.subheader("📈 Provider Price Comparison")

chart_df = comparison_df.set_index("Provider")

st.bar_chart(chart_df["Price"])

st.divider()

# --------------------------------------------------
# CHEAPEST OPTION
# --------------------------------------------------

st.subheader("🏆 Best Value Option")

st.success(
    f"""
    Cheapest Provider: **{cheapest_provider}**

    Lowest Available Price: **₹{min_price:.0f}**
    """
)

st.divider()

# --------------------------------------------------
# INTERPRETATION
# --------------------------------------------------

st.subheader("📌 Interpretation")

st.info(
    f"""
    The average market price for **{selected_test}**
    is approximately **₹{avg_price:.0f}**.

    Prices in the dataset range from **₹{min_price:.0f}**
    to **₹{max_price:.0f}** depending on the provider.

    **{cheapest_provider}** currently offers the lowest
    reported price for this test.

    Comparing costs before booking can help users
    reduce healthcare expenses and make informed decisions.
    """
)

st.divider()

st.caption(
    "Disclaimer: Prices are indicative and may vary based on location, package inclusions, laboratory policies, and consultation charges."
)

st.warning(
    """
    ⚠️ Demo Disclaimer

    The pricing data used in this module is illustrative and has been created for academic project purposes. Actual healthcare costs may differ significantly.
    """
)