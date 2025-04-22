import streamlit as st
import pandas as pd

# --- Basic Login ---
st.title(" Jail Informer – Red Flag Viewer")
password = st.text_input("Enter Access Password", type="password")

if password != "runsecure":
    st.warning("Access Denied. Enter correct password to view alerts.")
    st.stop()

# --- Upload CSV ---
uploaded_file = st.file_uploader("Upload Red Flag Alerts CSV", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # Clean data
    df = df.dropna(subset=["Call ID", "Summary"])
    df = df.loc[:, ~df.columns.str.contains(r'^\.\d+$')]

    st.subheader(" Filtered Alerts Table")

    # Sidebar filters
    st.sidebar.header("Filter Options")
    risk_levels = df["Risk Level"].dropna().unique().tolist()
    selected_levels = st.sidebar.multiselect("Risk Levels", risk_levels, default=risk_levels)
    follow_up_only = st.sidebar.checkbox("Show only Follow Up = Yes")

    # Apply filters
    filtered_df = df[df["Risk Level"].isin(selected_levels)]
    if follow_up_only:
        filtered_df = filtered_df[df["Follow Up"] == "Yes"]

    st.markdown(f"### Showing {len(filtered_df)} alerts")
    st.dataframe(filtered_df[[
        "Date", "Inmate", "Call ID", "Risk Level", "Risk Type",
        "Summary", "Follow Up", "Reviewed By", "Status"
    ]], use_container_width=True)

    st.download_button(
        label="Download Filtered CSV",
        data=filtered_df.to_csv(index=False),
        file_name="filtered_alerts.csv",
        mime="text/csv"
    )
