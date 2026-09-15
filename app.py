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
# FINDING DATE & TIME
# ==========================================

current_datetime = datetime.now(
    ZoneInfo("Asia/Kuala_Lumpur")
)

display_datetime = current_datetime.strftime(
    "%d-%b-%Y %H:%M:%S"
)

st.text_input(
    "Finding Date & Time",
    value=display_datetime,
    disabled=True
)


# ==========================================
# AREA
# ==========================================

area = st.selectbox(
    "Area",
    ["DP", "FOL", "MOL", "EOL"]
)


# ==========================================
# STATION
# Automatically changes based on Area
# ==========================================

station = st.selectbox(
    "Station",
    stations[area]
)


# ==========================================
# CATEGORY
# ==========================================

category = st.selectbox(
    "Category",
    [
        "Method / Handling - Incorrect process execution, setup, or operating method",
        "Machine / Facility - Ionizer, machine abnormal reading, equipment/facility condition",
        "Material / Product - Material condition, expiry, identification, mixed material",
        "Document / Record - Checklist, record, label, traceability, or documentation",
        "Personnel Compliance - Not following cleanroom, 5S, ESD, discipline requirement"
    ]
)


# ==========================================
# FINDING DESCRIPTION
# ==========================================

finding = st.text_area(
    "Finding Description",
    placeholder="Describe the IPQC finding..."
)


# ==========================================
# PRIORITY
# ==========================================

priority = st.selectbox(
    "Priority",
    [
        "Low",
        "Medium",
        "High"
    ]
)


# ==========================================
# OWNER
# ==========================================

owner = st.text_input(
    "Owner",
    placeholder="Enter owner name"
)


# ==========================================
# SUBMIT BUTTON
# ==========================================

submitted = st.button(
    "Submit Finding",
    type="primary",
    use_container_width=True
)


# ==========================================
# SUBMISSION
# ==========================================

if submitted:

    # Capture the actual submission time
    submitted_datetime = datetime.now(
        ZoneInfo("Asia/Kuala_Lumpur")
    )

    finding_datetime = submitted_datetime.strftime(
        "%d-%b-%Y %H:%M:%S"
    )

    # Basic validation
    if finding.strip() == "":
        st.error(
            "Please enter a Finding Description."
        )

    elif owner.strip() == "":
        st.error(
            "Please enter an Owner."
        )

    else:

        st.success(
            "Finding submitted successfully!"
        )

        st.subheader(
            "Submitted Finding"
        )

        st.write(
            "Finding Date & Time:",
            finding_datetime
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
