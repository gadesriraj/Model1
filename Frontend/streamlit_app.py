import streamlit as st
from datetime import datetime
import requests

# 🔗 Backend API URL (Render)
BACKEND_URL = "https://backend-a1v7.onrender.com"  # change if your URL is different

st.set_page_config(
    page_title="Clinical Note Generator",
    page_icon="🏥",
    layout="wide"
)

st.title("🏥 Clinical Note Generator")

st.caption("Infosys Internship Project – Cloud-connected prototype")

st.divider()

# -------- Input Fields --------
col1, col2 = st.columns(2)

with col1:
    name = st.text_input("Patient Name", value="John Doe")
    age = st.number_input("Age", min_value=0, max_value=120, value=45)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])

with col2:
    symptoms = st.text_area(
        "Symptoms",
        value="Cough, chest pain, and shortness of breath",
        height=100
    )
    scan_result = st.text_input(
        "Scan Result (optional)",
        value="X-ray indicates mild pneumonia"
    )

medical_history = st.text_area(
    "Medical History (optional)",
    value="Hypertension",
    height=80
)

st.divider()

# -------- Helper to call backend --------
def call_backend():
    payload = {
        "name": name,
        "age": age,
        "gender": gender,
        "symptoms": symptoms,
        "scan_result": scan_result if scan_result.strip() else "No imaging performed",
        "medical_history": medical_history if medical_history.strip() else "None"
    }

    try:
        resp = requests.post(f"{BACKEND_URL}/process_patient", json=payload, timeout=40)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.RequestException as e:
        return None, str(e)

# -------- Button + Output --------
if st.button("Generate Clinical Note", type="primary", use_container_width=True):
    if not name.strip():
        st.error("Please enter a patient name.")
    elif not symptoms.strip():
        st.error("Please enter symptoms.")
    else:
        with st.spinner("Contacting backend and generating note..."):
            result, error = call_backend()

        if error:
            st.error(f"Backend error: {error}")
        else:
            st.success("Clinical note generated from cloud backend ✅")
            st.divider()

            # Extract fields from backend JSON
            note = result["clinical_documentation"]["generated_note"]
            icd = result["clinical_documentation"]["icd_coding"]

            st.subheader("📋 Clinical Note")
            st.markdown(note)

            st.subheader("🧾 ICD-10 Coding")
            st.write(f"**Code:** {icd['code']}")
            st.write(f"**Description:** {icd['description']}")
            st.write(f"**Confidence:** {icd['confidence']:.2f}")

            with st.expander("View raw backend response"):
                st.json(result)

st.divider()
st.caption("Backend: " + BACKEND_URL)
