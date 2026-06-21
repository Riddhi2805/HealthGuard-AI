import streamlit as st
import pandas as pd
import pdfplumber
import google.generativeai as genai

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



# ======================================
# PAGE CONFIG
# ======================================

st.title(
    "🤖 AI Medical Report Analyzer"
)

st.write(
    "Upload your medical report and receive AI-powered health insights."
)

# ======================================
# GEMINI SETUP
# ======================================

genai.configure(
    api_key=st.secrets["GEMINI_API_KEY"]
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

# ======================================
# FILE UPLOAD
# ======================================

uploaded_file = st.file_uploader(
    "Upload Medical Report (PDF)",
    type=["pdf"]
)

if uploaded_file:

    report_text = ""

    with pdfplumber.open(
        uploaded_file
    ) as pdf:

        for page in pdf.pages:

            text = page.extract_text()

            if text:

                report_text += text

    st.success(
        "✅ Report Uploaded Successfully"
    )

    st.info(
    f"📄 Extracted {len(report_text.split())} words from report"
    )

    if len(report_text.strip()) < 50:

        st.error(
        "Unable to extract readable text from this PDF. Please upload a text-based medical report."
        )

        st.stop()

    if st.button(
        "🤖 Analyze Report"
    ):

        with st.spinner(
            "Analyzing Report..."
        ):
            report_text = report_text[:15000]

            prompt = f"""
                You are an AI healthcare assistant.

                Analyze the uploaded medical report.

                Provide:

                ## Simple Summary
                Explain the report in simple language.

                ## Key Findings
                List important observations.

                ## Potential Health Concerns
                Mention possible concerns if applicable.

                ## Recommended Follow-Up Tests
                Suggest relevant tests if needed.

                ## Lifestyle Recommendations
                Provide practical health suggestions.

                Important:
                - Use easy-to-understand language.
                - Do not diagnose diseases.
                - If the uploaded document is not a medical report, clearly state that.
                - Include a disclaimer that users should consult a healthcare professional.

                Medical Report:

                {report_text}
                """
            
            try:

                response = model.generate_content(
                    prompt
                )

            except Exception as e:

                st.error(
                    "Unable to analyze report. Please try again later."
                )
                st.stop()

        st.success(
            "Analysis Complete"
        )
        
        st.markdown(
            response.text
        )

       

# ======================================
# DISCLAIMER
# ======================================

st.warning(
    """
    ⚠️ This analysis is AI-generated and should not be considered medical advice.
    Always consult a qualified healthcare professional before making medical decisions.
    """
)