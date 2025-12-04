import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Clinical Note Generator", page_icon="🏥", layout="wide")

st.title("🏥 Clinical Note Generator (Demo)")

# Small required notice (kept minimal)
st.caption("Prototype for internship project. Not for real clinical use.")

st.divider()

# Input fields
patient_name = st.text_input("Patient Name")
patient_age = st.number_input("Age", min_value=0, max_value=120, value=30)
symptoms = st.text_area("Symptoms", height=100)

st.divider()

# Generate clinical note
if st.button("Generate Clinical Note"):
    if not patient_name.strip():
        st.error("Please enter a patient name.")
    elif not symptoms.strip():
        st.error("Please enter symptoms.")
    else:
        st.success("Clinical Note Generated")

        clinical_note = f"""
### 📋 Clinical Note

**Date:** {datetime.now().strftime("%d %B %Y, %I:%M %p")}

**Patient Name:** {patient_name}  
**Age:** {patient_age}

**Symptoms Reported:**  
{symptoms}

**Note:** This is a demonstration clinical note generated for the internship project.
"""

        st.markdown(clinical_note)


