import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="MACI Compliance Dashboard", layout="wide")

st.title("🌙 Maqasid AI Compliance Index (MACI)")
st.subheader("Technical Audit Dashboard")

# User Input
st.sidebar.header("Audit Input")
faith = st.sidebar.slider("Protection of Faith", 0, 10, 8)
life = st.sidebar.slider("Protection of Life", 0, 10, 9)
intellect = st.sidebar.slider("Protection of Intellect", 0, 10, 7)
lineage = st.sidebar.slider("Protection of Lineage", 0, 10, 10)
property_val = st.sidebar.slider("Protection of Property", 0, 10, 6)

total_score = faith + life + intellect + lineage + property_val

# Score Display
st.metric(label="Total MACI Score", value=f"{total_score} / 50")

# Radar Chart for Visualization
df = pd.DataFrame(dict(
    r=[faith, life, intellect, lineage, property_val],
    theta=['Faith', 'Life', 'Intellect', 'Lineage', 'Property']))
fig = px.line_polar(df, r='r', theta='theta', line_close=True)
fig.update_traces(fill='toself')

st.plotly_chart(fig)

if total_score >= 40:
    st.success("Status: HALAL COMPLIANT")
else:
    st.warning("Status: REMEDIATION REQUIRED")

# AS THE PAPER IS UNDER REVIEW FOR JOURNAL PUBLICATION THE ACTUAL CODES ARE NOT MADE PUBLIC. BUT THE APP OR AUDITOR IS MADE WITH ACTUAL CODE. AND HERE FOR PUBLIC IS JUST A SAMPLE AVAILABLE.
# THANK YOU FOR UNDERSTANDING.
