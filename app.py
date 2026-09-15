import streamlit as st
from datetime import datetime, date, time, timedelta
from zoneinfo import ZoneInfo
from supabase import create_client


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
# SUPABASE CONNECTION
# ==========================================

@st.cache_resource
def init_supabase():
    return create_client(
        st.secrets["SUPABASE_URL"],
        st.secrets["SUPABASE_KEY"]
    )


supabase = init_supabase()


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
# 2026 SHIFT ROSTER
# ==========================================

shift_roster = {

    # Q3
    date(2026, 6, 28): ("CCBBBCC", "DDAAADD"),
    date(2026, 7, 5):  ("AAADDDD", "BBBCCCC"),
    date(2026, 7, 12): ("AAAADDD", "BBBBCCC"),
    date(2026, 7, 19): ("BBBCCCC", "AAADDDD"),
    date(2026, 7, 26): ("BBBBCCC", "AAAADDD"),

    date(2026, 8, 2):  ("AAADDDD", "BBBCCCC"),
    date(2026, 8, 9):  ("AAAADDD", "BBBBCCC"),
    date(2026, 8, 16): ("BBBCCCC", "AAADDDD"),
    date(2026, 8, 23): ("BBBBCCC", "AAAADDD"),
    date(2026, 8, 30): ("AAADDDD", "BBBCCCC"),

    date(2026, 9, 6):  ("AAAADDD", "BBBBCCC"),
    date(2026, 9, 13): ("BBBCCCC", "AAADDDD"),
    date(2026, 9, 20): ("BBBBCCC", "AAAADDD"),

    # Q4
    date(2026, 9, 27): ("AADDDAA", "BBCCCBB"),

    date(2026, 10, 4):  ("DDDAAAA", "CCCBBBB"),
    date(2026, 10, 11): ("CCCCBBB", "DDDDAAA"),
    date(2026, 10, 18): ("CCCBBBB", "DDDAAAA"),
    date(2026, 10, 25): ("DDDDAAA", "CCCCBBB"),

    date(2026, 11, 1):  ("DDDAAAA", "CCCBBBB"),
    date(2026, 11, 8):  ("CCCCBBB", "DDDDAAA"),
    date(2026, 11, 15): ("CCCBBBB", "DDDAAAA"),
    date(2026, 11, 22): ("DDDDAAA", "CCCCBBB"),
    date(2026, 11, 29): ("DDDAAAA", "CCCBBBB"),

    date(2026, 12, 6):  ("CCCCBBB", "DDDDAAA"),
    date(2026, 12, 13): ("CCCBBBB", "DDDAAAA"),
    date(2026, 12, 20): ("DDDDAAA", "CCCCBBB"),
    date(2026, 12, 27): ("DDAAA", "CCBBB")
}


# ==========================================
# FUNCTION TO DETERMINE SHIFT
# ==========================================

def get_shift(current_datetime):

    current_time = current_datetime.time()

    day_start = time(6, 30)
    night_start = time(18, 30)

    # Determine DAY / NIGHT
    if day_start <= current_time < night_start:

        shift_type = "DAY"
        roster_date = current_datetime.date()

    else:

        shift_type = "NIGHT"

        # Before 6:30 AM belongs to previous night's shift
        if current_time < day_start:

            roster_date = (
                current_datetime.date()
                - timedelta(days=1)
            )

        else:

            roster_date = current_datetime.date()

    # Find correct roster week
    for week_start, patterns in shift_roster.items():

        days_difference = (
            roster_date - week_start
        ).days

        if 0 <= days_difference <= 6:

            day_pattern = patterns[0]
            night_pattern = patterns[1]

            if shift_type == "DAY":
                pattern = day_pattern
            else:
                pattern = night_pattern

            if days_difference < len(pattern):

                shift_letter = pattern[
                    days_difference
                ]

                return (
                    shift_letter,
                    shift_type
                )

    return ("N/A", shift_type)


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
# AUTOMATIC SHIFT
# ==========================================

shift_letter, shift_type = get_shift(
    current_datetime
)

shift_display = (
    f"{shift_letter} - {shift_type}"
)

st.text_input(
    "Shift",
    value=shift_display,
    disabled=True
)


# ==========================================
# AREA
# ==========================================

area = st.selectbox(
    "Area",
    ["DP", "FOL", "MOL", "EOL"],
    index=None,
    placeholder="Select Area"
)


# ==========================================
# STATION
# ==========================================

if area is not None:

    station = st.selectbox(
        "Station",
        stations[area],
        index=None,
        placeholder="Select Station"
    )

else:

    station = st.selectbox(
        "Station",
        [],
        index=None,
        placeholder="Select Area first",
        disabled=True
    )


# ==========================================
# EQUIPMENT / STATION ID
# ==========================================

equipment_id = st.text_input(
    "Equipment / Station ID",
    placeholder="E.g. ICO-02"
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
    ],
    index=None,
    placeholder="Select Category"
)


# ==========================================
# FINDING DESCRIPTION
# ==========================================

finding = st.text_area(
    "Finding Description",
    placeholder=(
        "During [when], [what] was observed at [where]. "
        "This does not meet [requirement]. "
        "Acknowledged by [supervisor/leader]."
    )
)


# ==========================================
# INTERVIEW RESULT
# ==========================================

interview_result = st.text_area(
    "Interview Result",
    placeholder=(
        "Enter explanation from auditee or supervisor"
    )
)


# ==========================================
# CONTAINMENT ACTION
# ==========================================

containment_action = st.text_area(
    "Containment Action",
    placeholder=(
        "Enter immediate containment action taken"
    )
)


# ==========================================
# AUDITEE
# ==========================================

auditee = st.text_input(
    "Auditee",
    placeholder="Enter auditee badge"
)


# ==========================================
# AUDITOR
# ==========================================

auditor = st.text_input(
    "Auditor",
    placeholder="Enter auditor badge"
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

    # --------------------------------------
    # VALIDATION
    # --------------------------------------

    if area is None:

        st.error(
            "Please select an Area."
        )

    elif station is None:

        st.error(
            "Please select a Station."
        )

    elif equipment_id.strip() == "":

        st.error(
            "Please enter an Equipment / Station ID."
        )

    elif category is None:

        st.error(
            "Please select a Category."
        )

    elif finding.strip() == "":

        st.error(
            "Please enter a Finding Description."
        )

    elif interview_result.strip() == "":

        st.error(
            "Please enter an Interview Result."
        )

    elif containment_action.strip() == "":

        st.error(
            "Please enter a Containment Action."
        )

    elif auditee.strip() == "":

        st.error(
            "Please enter an Auditee."
        )

    elif auditor.strip() == "":

        st.error(
            "Please enter an Auditor."
        )

    else:

        # ----------------------------------
        # CAPTURE ACTUAL SUBMISSION TIME
        # ----------------------------------

        submitted_datetime = datetime.now(
            ZoneInfo("Asia/Kuala_Lumpur")
        )

        finding_datetime = (
            submitted_datetime.strftime(
                "%d-%b-%Y %H:%M:%S"
            )
        )


        # ----------------------------------
        # RECALCULATE SHIFT AT SUBMISSION
        # ----------------------------------

        submitted_shift_letter, submitted_shift_type = (
            get_shift(submitted_datetime)
        )

        submitted_shift = (
            f"{submitted_shift_letter} - "
            f"{submitted_shift_type}"
        )


        # ----------------------------------
        # PREPARE DATABASE RECORD
        # ----------------------------------

        finding_record = {
            "finding_datetime": finding_datetime,
            "shift": submitted_shift,
            "area": area,
            "station": station,
            "equipment_id": equipment_id,
            "category": category,
            "finding_description": finding,
            "interview_result": interview_result,
            "containment_action": containment_action,
            "auditee": auditee,
            "auditor": auditor,
            "status": "Open"
        }


        # ----------------------------------
        # SAVE FINDING TO SUPABASE
        # ----------------------------------

        try:

            response = (
                supabase
                .table("Findings")
                .insert(
                    finding_record,
                    returning="minimal"
                )
                .execute()
            )


            # ----------------------------------
            # SUCCESS MESSAGE
            # ----------------------------------

            st.success(
                "Finding submitted successfully!"
            )


            # ----------------------------------
            # DISPLAY SUBMITTED RECORD
            # ----------------------------------

            st.subheader(
                "Submitted Finding"
            )

            st.write(
                "Finding Date & Time:",
                finding_datetime
            )

            st.write(
                "Shift:",
                submitted_shift
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
                "Equipment / Station ID:",
                equipment_id
            )

            st.write(
                "Category:",
                category
            )

            st.write(
                "Finding Description:",
                finding
            )

            st.write(
                "Interview Result:",
                interview_result
            )

            st.write(
                "Containment Action:",
                containment_action
            )

            st.write(
                "Auditee:",
                auditee
            )

            st.write(
                "Auditor:",
                auditor
            )

            st.write(
                "Status:",
                "Open"
            )


        # ----------------------------------
        # DATABASE ERROR
        # ----------------------------------

        except Exception as e:

            st.error(
                f"Supabase error: {e}"
            )
