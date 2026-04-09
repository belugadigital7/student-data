import streamlit as st
import pandas as pd
import os

# File to store data
DATA_FILE = "student_records.csv"

# Initialize data if file doesn't exist
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Student Name", "Subject", "Marks", "Attendance %"])
    df.to_csv(DATA_FILE, index=False)

def load_data():
    return pd.read_csv(DATA_FILE)

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# App UI
st.title("🎓 Student Register")

menu = ["View Register", "Add/Update Student", "Analytics"]
choice = st.sidebar.selectbox("Navigation", menu)

if choice == "View Register":
    st.subheader("Current Records")
    data = load_data()
    st.dataframe(data, use_container_width=True)

elif choice == "Add/Update Student":
    st.subheader("Edit Student Details")
    with st.form("student_form"):
        name = st.text_input("Student Name")
        subject = st.selectbox("Subject", ["Math", "Science", "History", "English"])
        marks = st.number_input("Marks", min_value=0, max_value=100)
        attendance = st.slider("Attendance %", 0, 100, 80)
        
        submit = st.form_submit_button("Save Record")
        
        if submit:
            df = load_data()
            new_row = {"Student Name": name, "Subject": subject, "Marks": marks, "Attendance %": attendance}
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            save_data(df)
            st.success(f"Record for {name} saved!")

elif choice == "Analytics":
    st.subheader("Performance Overview")
    df = load_data()
    if not df.empty:
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Average Marks", round(df["Marks"].mean(), 2))
        with col2:
            st.metric("Avg Attendance", f"{round(df['Attendance %'].mean(), 1)}%")
            
        st.bar_chart(df.set_index("Student Name")["Marks"])
    else:
        st.warning("No data available yet.")