import streamlit as st
from PIL import Image
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime
import json
import os

# Page setup
logo = Image.open("logo.png")
st.set_page_config(page_title="TnBcS Inquiry", page_icon=logo, layout="centered")

# Load credentials from Streamlit secrets
service_account_info = json.loads(st.secrets["GOOGLE_SERVICE_ACCOUNT"])
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
client = gspread.authorize(credentials)
sheet = client.open("TnBcS Prospects").sheet1

# Initialize session state
if 'form_submitted' not in st.session_state:
    st.session_state.form_submitted = False

# Show confirmation if submitted
if st.session_state.form_submitted:
    st.success("✅ Thank you! Our team will connect with you shortly.")
    st.markdown("You can close this tab or go back to the [TnBcS Home Page](https://tnbcs.framer.website).")
else:
    st.image("logo.png", width=120)
    st.title("Connect with TnBcS")
    st.write("We act as tunnels and bridges to overcome your business obstacles. Let’s build together!")
    st.markdown("Please fill out the form below. Our team will reach out to assist you.")

    with st.form("contact_form", clear_on_submit=False):
        name = st.text_input("Your Name *")
        company = st.text_input("Company Name")
        email = st.text_input("Email Address")
        phone = st.text_input("Phone Number *")
        service = st.selectbox("Service Interested In", [
            "CRM", "Outsourcing Vendor Cycle", "Recruitment Tracker",
            "Approval Request System", "Performance Management", "Attendance Tracker",
            "Project Management", "Sales-Design-Tooling-Production", "Financial Module",
            "Inventory Management", "Shipping Management", "Machine Planning",
            "Downtime Tracking", "One-click MIS", "Hotel Booking System", "Quotation", "Invoicing", "Other"
        ])
        message = st.text_area("Additional Message")

        submitted = st.form_submit_button("Submit")

        if submitted:
            if not name.strip() or not phone.strip():
                st.error("Please fill all required fields marked with *.")
            else:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet.append_row([timestamp, name, company, email, phone, service, message])
                st.session_state.form_submitted = True
                st.rerun()
