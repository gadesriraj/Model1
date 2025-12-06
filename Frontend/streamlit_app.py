import streamlit as st
from datetime import datetime
import requests

# 🔗 Backend API URL (Render)
BACKEND_URL = "https://backend-a1v7.onrender.com"  # change if your URL is different

# ---------- Page config ----------
st.set_page_config(
    page_title="Clinical Note Generator",
    page_icon="🏥",
    layout="wide"
)

# ---------- Title ----------
st.title("🏥 Clinical Note Generator")
st.caption("Infosys Internship Project – Cloud-connected prototype")

st.divider()

# ---------- Input layout ----------
col_left, col_right = st.columns(2)

with col_left:
    patient_name = st.text_input(
        "Patient Name",
        value="",
        placeholder="Enter patient name"
    )

    patient_age = st.number_input(
        "Age",
        min_value=0,
        max_value=120,
        value=0,
        step=1
    )

    gender = st.selectbox(
        "Gender",
        ["Select", "Male", "Female", "Other"],
        index=0
    )

    medical_history = st.text_area(
        "Medical History (optional)",
        value="",
        placeholder="e.g., Hypertension, Diabetes",
        height=80
    )

with col_right:
    symptoms = st.text_area(
        "Symptoms",
        value="",
        placeholder="Describe the patient's symptoms...",
        height=120
    )

    scan_result = st.text_input(
        "Scan Result (optional)",
        value="",
        placeholder="e.g., Chest X-ray shows mild pneumonia"
    )

st.divider()

# ---------- Helper: call backend ----------
def call_backend():
    payload = {
        "name": patient_name,
        "age": patient_age,
        "gender": gender if gender != "Select" else "Not specified",
        "symptoms": symptoms,
        "scan_result": scan_result if scan_result.strip() else "No imaging performed",
        "medical_history": medical_history if medical_history.strip() else "None"
    }

    resp = requests.post(
        f"{BACKEND_URL}/process_patient",
        json=payload,
        timeout=80
    )
    resp.raise_for_status()
    return resp.json()

# ---------- Button + validation + output ----------
if st.button("Generate Clinical Note", type="primary", use_container_width=True):

    # Basic validation
    if not patient_name.strip():
        st.error("Please enter a patient name.")
    elif patient_age <= 0:
        st.error("Please enter a valid age.")
    elif gender == "Select":
        st.error("Please select a gender.")
    elif not symptoms.strip():
        st.error("Please enter symptoms.")
    else:
        with st.spinner("Contacting backend and generating clinical note..."):
            try:
                result = call_backend()
                st.success("Clinical note generated successfully ✅")

                # Extract note + ICD info
                note = result["clinical_documentation"]["generated_note"]
                icd = result["clinical_documentation"]["icd_coding"]

                st.divider()

                # -------- Patient summary --------
                st.subheader("👤 Patient Summary")
                st.markdown(f"""
**Name:** {patient_name}  
**Age:** {patient_age}  
**Gender:** {gender}  

**Symptoms:** {symptoms}  
**Scan Result:** {scan_result or "Not provided"}  
**Medical History:** {medical_history or "None reported"}
                """)

                # -------- Clinical note --------
                st.subheader("📋 Generated Clinical Note")
                st.markdown(note)

                # -------- ICD-10 coding --------
                st.subheader("🧾 ICD-10 Coding")
                st.write(f"**Code:** {icd['code']}")
                st.write(f"**Description:** {icd['description']}")
                st.write(f"**Confidence:** {icd['confidence']:.2f}")

                # Raw response (for debugging / screenshots)
                with st.expander("View raw backend response (JSON)"):
                    st.json(result)

            except requests.exceptions.RequestException as e:
                st.error(f"Backend error: {e}")

st.divider()
st.caption("Backend: " + BACKEND_URL)

# --- Sidebar: Saved Records ---
with st.sidebar:
    st.header("🔍 View Saved Records")

    if st.button("Load Saved records"):
        try:
            resp = requests.get(f"{BACKEND_URL}/records", timeout=30)
            resp.raise_for_status()
            data = resp.json()

            st.success(f"Loaded {data['count']} records.")
            # show as table in sidebar (compact)
            st.dataframe(data["records"])
        except Exception as e:
            st.error(f"Error loading records: {e}")
