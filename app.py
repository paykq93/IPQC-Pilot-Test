import streamlit as st
from datetime import date

st.title("IPQC Finding Entry")

with st.form("finding_form"):

    finding_date = st.date_input(
        "Finding Date",
        value=date.today()
    )

    line = st.selectbox(
        "Line",
        ["Line 1", "Line 2", "Line 3"]
    )

    station = st.selectbox(
        "Station",
        ["Die Attach", "Wire Bond", "Mold", "Underfill"]
    )

    category = st.selectbox(
        "Category",
        ["Process", "Material", "Machine", "Method", "5S"]
    )

    finding = st.text_area("Finding Description")

    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High"]
    )

    owner = st.text_input("Owner")

    submitted = st.form_submit_button("Submit Finding")

if submitted:
    st.success("Finding submitted successfully!")

    st.write("Date:", finding_date)
    st.write("Line:", line)
    st.write("Station:", station)
    st.write("Category:", category)
    st.write("Finding:", finding)
    st.write("Priority:", priority)
    st.write("Owner:", owner)
