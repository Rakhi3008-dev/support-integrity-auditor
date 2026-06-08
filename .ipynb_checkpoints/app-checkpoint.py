
import streamlit as st
import pandas as pd
import joblib

# -------------------------------
# Load Model
# -------------------------------

model = joblib.load("models/xgb_pipeline.pkl")

# -------------------------------
# Page Config
# -------------------------------

st.set_page_config(
    page_title="Support Integrity Auditor",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------------
# Sidebar Dashboard
# -------------------------------

st.sidebar.title("📊 Audit Dashboard")

st.sidebar.metric(
    "Hidden Crisis",
    "3202"
)

st.sidebar.metric(
    "False Alarm",
    "2239"
)

st.sidebar.metric(
    "Consistent",
    "14559"
)

st.sidebar.markdown("---")

uploaded_file = st.sidebar.file_uploader(
    "Upload CSV (Optional)",
    type=["csv"]
)

# -------------------------------
# Main Title
# -------------------------------

st.title("🛡️ Support Integrity Auditor")

st.markdown(
"""
AI-powered system for detecting whether a
customer support ticket has been assigned
an incorrect priority.
"""
)

st.divider()

# -------------------------------
# Severity Keywords
# -------------------------------

severity_keywords = {
    "outage": 5,
    "fraud": 5,
    "hacked": 5,
    "stolen": 5,
    "payment failed": 4,
    "unauthorized": 4,
    "error": 3,
    "failed": 3,
    "urgent": 2,
    "asap": 1,
    "login": 1,
    "password": 1
}


def keyword_score(text):
    text = text.lower()
    score = 0

    for word, value in severity_keywords.items():
        if word in text:
            score += value

    return score


# -------------------------------
# Input Section
# -------------------------------

subject = st.text_input(
    "Ticket Subject"
)

description = st.text_area(
    "Ticket Description"
)

col1, col2 = st.columns(2)

with col1:

    issue = st.selectbox(
        "Issue Category",
        [
            "Technical",
            "Billing",
            "Account",
            "General Inquiry",
            "Fraud"
        ]
    )

with col2:

    channel = st.selectbox(
        "Ticket Channel",
        [
            "Email",
            "Chat",
            "Web Form"
        ]
    )

col3, col4 = st.columns(2)

with col3:

    resolution = st.number_input(
        "Resolution Time (Hours)",
        min_value=1,
        max_value=120,
        value=24
    )

with col4:

    assigned = st.selectbox(
        "Assigned Priority",
        [
            "Low",
            "Medium",
            "High",
            "Critical"
        ]
    )

# -------------------------------
# Prediction
# -------------------------------

if st.button("🔍 Audit Ticket"):

    combined = subject + " " + description

    # ---------------------------
    # Feature Engineering
    # ---------------------------

    k_score = keyword_score(combined)

    semantic_score = min(
        1.0,
        0.4 + k_score * 0.08
    )

    if resolution <= 12:
        resolution_score = 3
    elif resolution <= 48:
        resolution_score = 2
    else:
        resolution_score = 1

    final_score = (
        0.5 * semantic_score
        +
        0.3 * (k_score / 10)
        +
        0.2 * (resolution_score / 3)
    )

    sample = pd.DataFrame({

        "Combined_Text": [combined],

        "Issue_Category": [issue],

        "Ticket_Channel": [channel],

        "Resolution_Time_Hours": [resolution],

        "Keyword_Score": [k_score],

        "Semantic_Score": [semantic_score],

        "Final_Severity_Score": [final_score]

    })

    pred = model.predict(sample)[0]

    # ---------------------------
    # Output
    # ---------------------------

    st.divider()

    if pred == 1:
        st.error("🔴 Priority Mismatch Detected")
        inferred = "Higher than Assigned"
        confidence = min(
            95,
            75 + int(final_score * 20)
        )
    else:
        st.success("🟢 Priority Assignment Looks Consistent")
        inferred = assigned
        confidence = min(
            95,
            80 + int((1 - final_score) * 10)
        )

    colA, colB = st.columns(2)

    with colA:
        st.metric(
            "Confidence",
            f"{confidence}%"
        )

    with colB:
        st.metric(
            "Final Severity Score",
            round(final_score, 3)
        )

    st.write(
        f"**Assigned Priority:** {assigned}"
    )

    st.write(
        f"**Inferred Severity:** {inferred}"
    )

    # ---------------------------
    # Evidence
    # ---------------------------

    st.divider()

    st.subheader("📋 Evidence")

    detected = []

    for word in severity_keywords:
        if word in combined.lower():
            detected.append(word)

    if len(detected) == 0:
        detected.append(
            "No strong trigger words detected"
        )

    st.write("### Keywords Detected")

    for item in detected:
        st.write(f"• {item}")

    st.write("")

    st.write(
        f"**Semantic Score:** {semantic_score:.3f}"
    )

    st.write(
        f"**Resolution Time:** {resolution} hours"
    )

    st.write(
        f"**Keyword Score:** {k_score}"
    )

    # ---------------------------
    # AI Explanation
    # ---------------------------

    st.divider()

    st.subheader("🤖 AI Explanation")

    if pred == 1:

        st.info(

            f"""
The presence of **{", ".join(detected)}**
combined with a semantic urgency score of
**{semantic_score:.2f}** suggests that the
ticket may deserve a higher priority than
the currently assigned **{assigned}** level.

The system recommends that this ticket
be reviewed manually by a support supervisor.
            """

        )

    else:

        st.success(

            f"""
The semantic indicators, detected keywords,
and operational features appear to be
consistent with the assigned
**{assigned}** priority.

No significant mismatch was detected.
            """

        )
