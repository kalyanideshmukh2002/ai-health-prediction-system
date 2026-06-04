import streamlit as st
import sqlite3
import pandas as pd
st.set_page_config(
    page_title="AI Health Prediction System",
    layout="wide"
)

# Database Connection
conn = sqlite3.connect("health.db", check_same_thread=False)
cursor = conn.cursor()

# Table Create
cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    dob TEXT,
    email TEXT,
    glucose REAL,
    hemoglobin REAL,
    cholesterol REAL,
    remarks TEXT
)
""")

conn.commit()

# Prediction Function
def predict_health(glucose, cholesterol, hemoglobin):

    if glucose > 180 and cholesterol > 240:
        return "High Risk of Diabetes and Heart Disease"

    elif hemoglobin < 8:
        return "Possible Anemia Risk"

    elif glucose > 140:
        return "High Diabetes Risk"

    elif cholesterol > 240:
        return "Heart Disease Risk"

    else:
        return "Normal"

# Title
st.title("AI-Based Health Prediction App")
st.sidebar.title("Navigation")
menu = ["Add Patient", "View Patients", "Update Patient", "Delete Patient"]
choice = st.sidebar.selectbox("Menu", menu)

# Add Patient
if choice == "Add Patient":

    st.subheader("Enter Patient Details")

    name = st.text_input("Full Name")
    dob = st.date_input("Date of Birth")
    email = st.text_input("Email")

    glucose = st.number_input("Glucose")
    hemoglobin = st.number_input("Hemoglobin")
    cholesterol = st.number_input("Cholesterol")

    if st.button("Save Patient"):

        # Validation
        if "@" not in email:
            st.error("Invalid Email")
            

        else:
            remarks = predict_health(glucose, cholesterol,hemoglobin)

            cursor.execute("""
            INSERT INTO patients
            (name, dob, email, glucose, hemoglobin, cholesterol, remarks)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                name,
                str(dob),
                email,
                glucose,
                hemoglobin,
                cholesterol,
                remarks
            ))

            conn.commit()

            st.success("Patient Saved Successfully")
            st.write("Prediction:", remarks)

# View Patients
elif choice == "View Patients":

    st.subheader("Patient Records")

    data = pd.read_sql("SELECT * FROM patients", conn)

    st.dataframe(data)
    
    # Update Patient
elif choice == "Update Patient":

    st.subheader("Update Patient")

    patient_id = st.number_input("Enter Patient ID", step=1)

    new_glucose = st.number_input("New Glucose")
    new_cholesterol = st.number_input("New Cholesterol")

    if st.button("Update"):

        new_remarks = predict_health(new_glucose, new_cholesterol)

        cursor.execute("""
        UPDATE patients
        SET glucose=?,
            cholesterol=?,
            remarks=?
        WHERE id=?
        """, (
            new_glucose,
            new_cholesterol,
            new_remarks,
            patient_id
        ))

        conn.commit()

        st.success("Patient Updated Successfully")
        # Delete Patient
elif choice == "Delete Patient":

    st.subheader("Delete Patient")

    patient_id = st.number_input("Enter Patient ID to Delete", step=1)

    if st.button("Delete"):

        cursor.execute(
            "DELETE FROM patients WHERE id=?",
            (patient_id,)
        )

        conn.commit()

        st.success("Patient Deleted Successfully")
        st.markdown("---")
st.caption(
    "Developed using Python, Streamlit and SQLite"
)