import gspread
import pandas as pd
from google.oauth2.service_account import Credentials

# Path to your service account credentials
SERVICE_ACCOUNT_FILE = "blsh_dashboard/streamlit.json"

# ✅ Updated scopes for both reading and accessing drive files
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Load credentials and authorize client
import streamlit as st
creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=SCOPES)

client = gspread.authorize(creds)

def get_sheet_data(sheet_name: str) -> pd.DataFrame:
    """Fetch live data from Google Sheet and return as DataFrame."""
    try:
        sheet = client.open("BLSH_Bills and Data").worksheet(sheet_name)
        data = sheet.get_all_records()

        # Handle empty sheet case
        if not data:
            print(f"⚠️ No data found in sheet: {sheet_name}")
            return pd.DataFrame()

        df = pd.DataFrame(data)
        return df

    except Exception as e:
        print(f"❌ Error fetching data from sheet '{sheet_name}': {e}")
        return pd.DataFrame()
