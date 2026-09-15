import streamlit as st
from datetime import date

st.title("IPQC Finding Entry")

# Station list based on Area
stations = {
    "DP": [
        "IWI",
        "Wafer Backgrind",
        "Wafer Mount",
        "Laser Trench",
        "Sawing",
        "UV",
        "Pick & Place",
        "Die Bank",
        "Waffle Pack Cleaning"
    ],

    "FOL": [
        "2nd Opt Inspection",
        "Substrate Bake",
        "Solder Paste Printing",
        "Chip Cap Attach",
        "Imprint Printing",
        "Flip Chip Attach",
        "Single Reflow",
        "Flux Cleaning",
        "X-Ray"
    ],

    "MOL": [
        "Prebake Oven",
        "Plasma",
        "Underfill Dispense",
        "Pressure Cure",
        "UF CSAM",
        "AOI"
    ],

    "EOL": [
        "Adhesive Dispense",
        "Stiffener/Lid Attach",
        "Indium Attach & Reflow",
        "Solder Ball Mount & Reflow",
        "Open Short",
        "ICOS",
        "Assy VM"
    ]
}

# These are OUTSIDE the form so they update immediately
area = st.selectbox(
    "Area",
    ["DP", "FOL", "MOL", "EOL"]
)

station = st.selectbox(
    "Station",
    stations[area]
)

# Main form
with st.form("finding_form"):

    finding_date = st.date_input(
        "Finding Date",
        value=date.today()
    )

    category = st.selectbox(
        "Category",
        ["Process", "Material", "Machine", "Method", "5S"]
    )

    finding = st.text_area(
        "Finding Description"
    )

    priority = st.selectbox(
        "Priority",
        ["Low", "Medium", "High"]
    )

    owner = st.text_input(
        "Owner"
    )

    submitted = st.form_submit_button(
        "Submit Finding"
    )


if submitted:
    st.success("Finding submitted successfully!")

    st.write("Date:", finding_date)
    st.write("Area:", area)
    st.write("Station:", station)
    st.write("Category:", category)
    st.write("Finding:", finding)
    st.write("Priority:", priority)
    st.write("Owner:", owner)
