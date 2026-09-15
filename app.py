import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo


# ==========================================
# PAGE SETUP
# ==========================================

st.set_page_config(
    page_title="IPQC Finding Entry",
    page_icon="🔍",
    layout="centered"
)

st.title("IPQC Finding Entry")


# ==========================================
# STATION LIST BY AREA
# ==========================================

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


# ==========================================
# AREA
# ==========================================

area = st.selectbox(
    "Area",
    ["DP", "FOL", "MOL", "EOL"]
)


# ==========================================
# STATION
# Station automatically changes with Area
# ==========================================

station = st.selectbox(
    "Station",
    stations[area]
)


# ==========================================
# FINDING FORM
# ==========================================

with st.form("finding_form"):

    category = st.selectbox(
        "Category",
        [
            "Process",
            "Material",
            "Machine",
            "Method",
            "5S"
        ]
    )

    finding = st.text_area(
        "Finding Description",
        placeholder="Describe the IPQC finding..."
    )

    priority = st.selectbox(
        "Priority",
        [
            "Low",
            "Medium",
            "High"
        ]
    )

    owner = st.text_input(
        "Owner",
        placeholder="Enter owner name"
    )

    submitted = st.form_submit_button(
        "Submit Finding"
    )


# ==========================================
# SUBMISSION
# ==========================================

if submitted:

    # Automatically capture Malaysia date & time
    finding_datetime = datetime.now(
        ZoneInfo("Asia/Kuala_Lumpur")
    )

    # Format:
    # 15-Sep-2026 14:08:37
    finding_datetime_formatted = finding_datetime.strftime(
        "%d-%b-%Y %H:%M:%S"
    )

    st.success("Finding submitted successfully!")

    st.subheader("Submitted Finding")

    st.write(
        "Finding Date & Time:",
        finding_datetime_formatted
    )

    st.write(
        "Area:",
        area
    )

    st.write(
        "Station:",
        station
    )

    st.write(
        "Category:",
        category
    )

    st.write(
        "Finding:",
        finding
    )

    st.write(
        "Priority:",
        priority
    )

    st.write(
        "Owner:",
        owner
    )
