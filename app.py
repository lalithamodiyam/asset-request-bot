import streamlit as st
import json
import sqlite3
import uuid
import pandas as pd

st.set_page_config(
    page_title="Asset Request Bot",
    page_icon="💻",
    layout="wide"
)

# Database Connection
conn = sqlite3.connect("requests.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS requests(
ticket_id TEXT,
employee_id TEXT,
employee_name TEXT,
role TEXT,
grade TEXT,
asset_type TEXT,
asset_name TEXT,
reason TEXT,
urgency TEXT,
status TEXT
)
""")

conn.commit()

# Load HRIS Data
with open("employees.json", "r") as file:
    employees = json.load(file)

st.title("💻 Service Desk - Asset Request Bot")
st.markdown("Automated Asset Request Management System")

tab1, tab2 = st.tabs(["📝 New Request", "📋 Request History"])

# ---------------- NEW REQUEST TAB ----------------

with tab1:

    st.subheader("Create Asset Request")

    employee_id = st.text_input("Employee ID")

    if employee_id:

        if employee_id in employees:

            emp = employees[employee_id]

            st.success("✅ Employee Validated")

            col1, col2, col3 = st.columns(3)

            col1.metric("Employee", emp["name"])
            col2.metric("Role", emp["role"])
            col3.metric("Grade", emp["grade"])

            asset_type = st.selectbox(
                "Asset Type",
                ["Laptop", "Software License"]
            )

            asset_name = st.text_input("Asset Name")

            urgency = st.selectbox(
                "Urgency",
                ["Low", "Medium", "High"]
            )

            reason = st.text_area("Reason for Request")

            if st.button("Submit Request"):

                ticket_id = "TKT-" + str(uuid.uuid4())[:8]

                if emp["grade"] in ["G4", "G5", "G6", "G7"]:
                    status = "Approved"
                else:
                    status = "Pending Approval"

                cursor.execute("""
                INSERT INTO requests VALUES
                (?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    ticket_id,
                    employee_id,
                    emp["name"],
                    emp["role"],
                    emp["grade"],
                    asset_type,
                    asset_name,
                    reason,
                    urgency,
                    status
                ))

                conn.commit()

                request_json = {
                    "ticket_id": ticket_id,
                    "employee_id": employee_id,
                    "employee_name": emp["name"],
                    "role": emp["role"],
                    "grade": emp["grade"],
                    "asset_type": asset_type,
                    "asset_name": asset_name,
                    "reason": reason,
                    "urgency": urgency,
                    "status": status
                }

                st.success("🎉 Request Submitted Successfully")

                st.write("### Request Summary")
                st.write(f"**Ticket ID:** {ticket_id}")
                st.write(f"**Employee:** {emp['name']}")
                st.write(f"**Asset:** {asset_name}")
                st.write(f"**Urgency:** {urgency}")
                st.write(f"**Status:** {status}")

                with st.expander("📄 View Generated JSON"):
                    st.json(request_json)

        else:
            st.error("❌ Invalid Employee ID")

# ---------------- REQUEST HISTORY TAB ----------------

with tab2:

    st.subheader("Request History")

    try:
        data = pd.read_sql_query(
            "SELECT * FROM requests",
            conn
        )

        st.dataframe(data, use_container_width=True)

    except:
        st.info("No requests available.")